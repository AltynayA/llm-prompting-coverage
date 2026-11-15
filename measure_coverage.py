import json
import subprocess
import shutil
import csv
import re
from pathlib import Path

BASE = Path(__file__).parent
FUNCTIONS_FILE = BASE / "code_under_test" / "functions.json"
GENERATED_DIR = BASE / "generated_tests"
WORK_DIR = BASE / "_coverage_work"
RESULTS_FILE = BASE / "results.csv"

STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]


def load_functions():
    with open(FUNCTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def run_one(func_name: str, code: str, strategy: str):
    test_path = GENERATED_DIR / strategy / f"{func_name}.py"
    if not test_path.exists():
        return {
            "function_name": func_name, "strategy": strategy,
            "coverage_percent": None, "lines_covered": None, "lines_total": None,
            "test_status": "MISSING", "notes": "no generated test file found"
        }

    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    WORK_DIR.mkdir(parents=True)

    module_file = WORK_DIR / "module_under_test.py"
    module_file.write_text(code, encoding="utf-8")

    #  sanitize imports in the generated test 
    generated_test_code = test_path.read_text(encoding="utf-8")
    generated_test_code = re.sub(
        r"^\s*(from\s+\S+\s+import\s+.*|import\s+.*)$",
        "", generated_test_code, flags=re.MULTILINE
    )
    test_file = WORK_DIR / "test_generated.py"
    test_file.write_text(
        "import sys, pathlib\n"  
        "sys.path.insert(0, str(pathlib.Path(__file__).parent))\n"
        "import pytest\n"  
        "from module_under_test import *\n\n"
        + generated_test_code,
        encoding="utf-8"
    )

    subprocess.run(["coverage", "erase"], cwd=WORK_DIR, capture_output=True)

    # 
    run = subprocess.run(
        ["coverage", "run", "--source=.", "-m", "pytest",
         "test_generated.py", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=WORK_DIR, capture_output=True, text=True, timeout=30
    )

    # status classifier
    notes = ""
    invalid_coverage = False
    if run.returncode == 0:
        status = "SUCCESS"
    elif run.returncode == 1:
        status = "TEST_FAILURES"
    elif run.returncode == 5 or "no tests ran" in run.stdout:
        status = "NO_TESTS"
        invalid_coverage = True
        notes = "pytest collected 0 tests — coverage invalid"
    elif "ModuleNotFoundError" in (run.stdout + run.stderr):
        status = "IMPORT_ERROR"
        invalid_coverage = True
        notes = (run.stderr or run.stdout)[-500:]
    else:
        status = "RUN_ERROR"
        invalid_coverage = True
        notes = (run.stderr or run.stdout)[-500:]

    json_report = WORK_DIR / "coverage.json"
    subprocess.run(["coverage", "json", "-o", str(json_report)], cwd=WORK_DIR, capture_output=True)

    # null out invalid coverage 
    coverage_percent, lines_covered, lines_total = None, None, None
    if not invalid_coverage and json_report.exists():
        try:
            data = json.loads(json_report.read_text())
            file_data = data["files"].get("module_under_test.py")
            if file_data:
                coverage_percent = round(file_data["summary"]["percent_covered"], 1)
                lines_covered = file_data["summary"]["covered_lines"]
                lines_total = file_data["summary"]["num_statements"]
        except Exception as e:
            status = "PARSE_ERROR"
            notes = str(e)

    return {
        "function_name": func_name, "strategy": strategy,
        "coverage_percent": coverage_percent,
        "lines_covered": lines_covered, "lines_total": lines_total,
        "test_status": status, "notes": notes
    }


def main():
    functions = load_functions()
    results = []

    for func in functions:
        name = func["func_name"]
        code = func["code"]
        print(f"\nMeasuring: {name}")
        for strategy in STRATEGIES:
            print(f"  [{strategy}] running coverage...")
            result = run_one(name, code, strategy)
            print(f"  [{strategy}] {result['test_status']} - {result['coverage_percent']}")
            results.append(result)

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "function_name", "strategy", "coverage_percent",
            "lines_covered", "lines_total", "test_status", "notes"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone! Results saved to {RESULTS_FILE}")
    print(f"Total rows: {len(results)} (expected 30)")

    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)


if __name__ == "__main__":
    main()