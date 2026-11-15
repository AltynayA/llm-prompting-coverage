import ast
import csv
import json
import os
import re
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# configuration
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found (check .env or export it)")

MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 8000          # thinking + answer share this budget
MAX_ATTEMPTS = 3           # same rule for every strategy
BUDGET_USD = 2.50          # hard stop if estimated spend passes this
PRICE_IN, PRICE_OUT = 2.00, 10.00   # USD per 1M tokens (Sonnet 5.5)
PLACEHOLDER = "{function_code}"
STRATEGIES = ["zero_shot", "few_shot", "chain_of_thought"]

BASE = Path(__file__).parent
FUNCTIONS_FILE = BASE / "code_under_test" / "functions.json"
PROMPTS_DIR = BASE / "prompts"
OUTPUT_DIR = BASE / "generated_tests"
LOG_FILE = BASE / "experiment_log.txt"
GEN_CSV = BASE / "generation_log.csv"

client = Anthropic(api_key=API_KEY)
spent_usd = 0.0


# helpers
def load_functions():
    with open(FUNCTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(strategy):
    return (PROMPTS_DIR / f"{strategy}.txt").read_text(encoding="utf-8")


def call_claude(prompt):
    msg = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "\n".join(b.text for b in msg.content if b.type == "text")
    return text, msg.stop_reason, msg.usage.input_tokens, msg.usage.output_tokens


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.DOTALL)
    return ("\n\n".join(blocks) if blocks else text).strip()


def validate(code):
    if not code:
        return False, "EMPTY"
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"SYNTAX_ERROR: {e.msg}"
    has_test = any(
        isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        for n in ast.walk(tree)
    )
    return (True, "OK") if has_test else (False, "NO_TEST_FUNCTIONS")


def log_attempt(row):
    new = not GEN_CSV.exists()
    with open(GEN_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "timestamp", "function_name", "strategy", "attempt",
            "stop_reason", "input_tokens", "output_tokens", "status"])
        if new:
            w.writeheader()
        w.writerow(row)


# main
def main():
    global spent_usd
    functions = load_functions()
    print(f"Loaded {len(functions)} functions | model={MODEL} | max_tokens={MAX_TOKENS}")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"\n=== Run started {time.strftime('%Y-%m-%d %H:%M:%S')} "
                  f"model={MODEL} max_tokens={MAX_TOKENS} ===\n")

        for func in functions:
            name, code = func["func_name"], func["code"]
            print(f"\nProcessing: {name}")

            for strategy in STRATEGIES:
                out_dir = OUTPUT_DIR / strategy
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / f"{name}.py"
                if out_file.exists():
                    print(f"  [{strategy}] exists - skipping")
                    continue

                prompt = load_template(strategy).replace(PLACEHOLDER, code)
                saved = False

                for attempt in range(1, MAX_ATTEMPTS + 1):
                    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        text, stop, tin, tout = call_claude(prompt)
                    except Exception as e:
                        status = f"API_ERROR: {e}"
                        print(f"  [{strategy}] attempt {attempt}: {status}")
                        log_attempt(dict(timestamp=stamp, function_name=name, strategy=strategy,
                                         attempt=attempt, stop_reason="", input_tokens="",
                                         output_tokens="", status=status[:120]))
                        time.sleep(3)
                        continue

                    spent_usd += tin * PRICE_IN / 1e6 + tout * PRICE_OUT / 1e6
                    if spent_usd > BUDGET_USD:
                        print(f"\nBUDGET GUARD: estimated spend ${spent_usd:.2f} > ${BUDGET_USD}. Stopping.")
                        log.write(f"BUDGET_GUARD stop at ${spent_usd:.2f}\n")
                        return

                    if stop == "max_tokens":
                        status = "TRUNCATED"
                    else:
                        code_out = extract_code(text)
                        ok, reason = validate(code_out)
                        status = "SUCCESS" if ok else reason

                    log_attempt(dict(timestamp=stamp, function_name=name, strategy=strategy,
                                     attempt=attempt, stop_reason=stop, input_tokens=tin,
                                     output_tokens=tout, status=status))
                    log.write(f"{name} | {strategy} | attempt {attempt} | {status}\n")
                    print(f"  [{strategy}] attempt {attempt}: {status} "
                          f"(out_tokens={tout}, stop={stop}, spent=${spent_usd:.3f})")

                    if status == "SUCCESS":
                        out_file.write_text(code_out + "\n", encoding="utf-8")
                        saved = True
                        break
                    time.sleep(1)

                if not saved:
                    log.write(f"{name} | {strategy} | GENERATION_FAILED after {MAX_ATTEMPTS} attempts\n")
                    print(f"  [{strategy}] GENERATION_FAILED - no file saved")
                time.sleep(1)

    n = len(list(OUTPUT_DIR.glob("*/*.py")))
    print(f"\nDone. {n}/30 files in generated_tests/. See generation_log.csv and experiment_log.txt")


if __name__ == "__main__":
    main()