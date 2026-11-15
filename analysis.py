import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.contingency_tables import cochrans_q

df = pd.read_csv("results.csv")
order = ["zero_shot", "few_shot", "chain_of_thought"]
wide = df.pivot(index="function_name", columns="strategy",
                values="coverage_percent")[order]
n, k = wide.shape
assert wide.notna().all().all(), "missing coverage values"

print("DESCRIPTIVES")
print(wide.agg(["mean", "median", "std", "min", "max"]).round(2).T)

print("\nSHAPIRO-WILK ON PAIRED DIFFERENCES")
for a, b in [("few_shot", "zero_shot"),
             ("chain_of_thought", "zero_shot"),
             ("chain_of_thought", "few_shot")]:
    d = wide[a] - wide[b]
    if d.nunique() < 2:
        print(a, "-", b, ": all differences identical, test not possible")
    else:
        w, p = stats.shapiro(d)
        print(a, "-", b, f": W = {w:.3f}, p = {p:.4f}")

print("\nFRIEDMAN (primary)")
chi2, p = stats.friedmanchisquare(*[wide[c] for c in order])
print(f"chi2({k-1}) = {chi2:.2f}, p = {p:.3f}, Kendall W = {chi2/(n*(k-1)):.2f}")

print("\nREPEATED-MEASURES ANOVA (check)")
print(AnovaRM(df, "coverage_percent", "function_name",
              within=["strategy"]).fit())

print("\nPASSING SUITES (exploratory)")
ok = (df.assign(ok=(df.test_status == "SUCCESS").astype(int))
        .pivot(index="function_name", columns="strategy", values="ok")[order])
print(ok.sum())
q = cochrans_q(ok.values)
print(f"Cochran Q({k-1}) = {q.statistic:.2f}, p = {q.pvalue:.3f}")