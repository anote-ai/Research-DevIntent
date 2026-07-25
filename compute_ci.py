"""Compute 95% bootstrap confidence intervals on overall IVR for each model."""
import json
import numpy as np

N_BOOTSTRAP = 10000

RESULT_FILES = {
    "Claude Sonnet 4.6": "results/experiment1.json",
    "GPT-4.1": "results/experiment1_gpt-4_1.json",
}


def per_problem_ivrs(per_task):
    ivrs = []
    for task_id, solutions in per_task.items():
        c1_passers = [s for s in solutions if s["passes_stated"]]
        if not c1_passers:
            continue
        n_violations = sum(1 for s in c1_passers if len(s["failed_hidden"]) > 0)
        ivrs.append(n_violations / len(c1_passers))
    return ivrs


def bootstrap_ci(ivrs, n_bootstrap=N_BOOTSTRAP):
    ivrs = np.array(ivrs)
    n = len(ivrs)
    means = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample = np.random.choice(ivrs, size=n, replace=True)
        means[i] = sample.mean()
    lower, upper = np.percentile(means, [2.5, 97.5])
    return lower, upper


def main():
    for model_name, path in RESULT_FILES.items():
        with open(path) as f:
            data = json.load(f)

        ivrs = per_problem_ivrs(data["per_task"])
        n = len(ivrs)
        point_estimate = sum(ivrs) / n

        np.random.seed(42)
        lower, upper = bootstrap_ci(ivrs)

        print(
            f"{model_name}: IVR = {point_estimate * 100:.1f}% "
            f"(95% CI: {lower * 100:.1f}%–{upper * 100:.1f}%), n={n}"
        )


if __name__ == "__main__":
    main()
