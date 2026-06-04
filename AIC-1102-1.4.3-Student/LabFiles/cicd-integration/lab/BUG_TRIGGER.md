# Trigger a Test Failure

The starter test suite passes. To exercise the Copilot CLI diagnostic workflow you will extend in Core Step 3, you need a deliberately failing test.

## Recommended Bug

Apply this single-line change to `src/stats.py` when you want to trigger a failure:

```diff
 def variance(values: list[float]) -> float:
     """Return the population variance of ``values``. Raises on empty input."""
     if not values:
         raise ValueError("values must be non-empty")
     m = mean(values)
-    return sum((v - m) ** 2 for v in values) / len(values)
+    return sum((v - m) ** 2 for v in values) / (len(values) - 1)
```

This swaps population variance (`/n`) for sample variance (`/(n-1)`). The bug is:

- **Subtle enough** that Copilot CLI must reason about the test assertion to identify it (`test_variance_basic` asserts `4`; the bug produces `4.571...`).
- **Not a crash** — no traceback, just a wrong answer — so the diagnosis must reason from the *failing assertion*, not from a stack trace.
- **A real category of bug** — the distinction between `/n` and `/(n-1)` is the single most common bug in statistics code.

## How to Apply

Commit the change on a branch and push. The CI workflow triggers on push and pull request.

```bash
git checkout -b trigger-bug
# apply the diff above to src/stats.py
git add src/stats.py
git commit -m "trigger: introduce variance bug for Copilot CLI diagnostic demo"
git push origin trigger-bug
```

Open a pull request from `trigger-bug` to `main`. The workflow runs, tests fail, and — after you complete Core Step 3 — Copilot CLI's diagnosis appears as a workflow artifact.

## Reverting

When you are done with the demo, drop the commit:

```bash
git checkout main
git branch -D trigger-bug
```

Do **not** merge the trigger branch. It exists only to exercise the workflow.
