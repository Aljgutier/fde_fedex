
# Starter Errors

The starter has:
* A syntax-level error in pricing.py that breaks import for any test module that imports pricing. Pytest reports it as a collection error.
* A logic error in inventory.py — an operator is off by one class (> where >= is correct).
* A state-leak bug in inventory.py — a class-level mutable default makes every Inventory instance share state. This is the lab’s signature symptom-vs.-root-cause trap.
* A performance issue in inventory.py that does not cause any test to fail but is visible on review.

# Test with the Initial Errors

```sh
pytest --tb=short
#--tb = traceback style
# short = show a condensed version of the error trace
```

* 2 import errors
* 2 test errors


```text
    ============================= test session starts =============================
    platform win32 -- Python 3.13.13, pytest-9.0.1, pluggy-1.6.0
    rootdir: C:\LabFiles\fde_repo\debugging-refactoring\lab
    collected 0 items / 3 errors

    =================================== ERRORS ====================================
    _____________________ ERROR collecting tests/test_cart.py _____________________
    ImportError while importing test module 'C:\LabFiles\fde_repo\debugging-refactoring\lab\tests\test_cart.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    C:\Users\labadmin\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\Lib\importlib\__init__.py:88: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    tests\test_cart.py:3: in <module>
        from cart import Cart
    E   ModuleNotFoundError: No module named 'cart'
    __________________ ERROR collecting tests/test_inventory.py ___________________
    ImportError while importing test module 'C:\LabFiles\fde_repo\debugging-refactoring\lab\tests\test_inventory.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    C:\Users\labadmin\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\Lib\importlib\__init__.py:88: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    tests\test_inventory.py:1: in <module>
        from inventory import Inventory
    E   ModuleNotFoundError: No module named 'inventory'
    ___________________ ERROR collecting tests/test_pricing.py ____________________
    ImportError while importing test module 'C:\LabFiles\fde_repo\debugging-refactoring\lab\tests\test_pricing.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    C:\Users\labadmin\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\Lib\importlib\__init__.py:88: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    tests\test_pricing.py:3: in <module>
        from models import Item
    E   ModuleNotFoundError: No module named 'models'
    =========================== short test summary info ===========================
    ERROR tests/test_cart.py
    ERROR tests/test_inventory.py
    ERROR tests/test_pricing.py
    !!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
    ============================== 3 errors in 0.09s ==============================
```

# 10.3.1 Autonomous Fix Loop

* The autonomous fix loop is the kind of thing Agent Mode does willingly — read failures, edit code, re-run tests, repeat until green. 
*  It is also where the most concealed debt gets introduced, because the agent will happily achieve a green suite by fixing the tests rather than the code.
* This subsection runs the loop without intervention so you can see what Copilot produces unsupervised
* the next subsection audits whether those changes are root-cause fixes or symptom-level ones.


prompt 
```
The test suite in this repository is failing. Run pytest, read the
failures, locate the bugs, and fix them. Do not modify the test
files. After each fix, re-run the tests and continue until all
tests pass.
```

**Fix Notes**

* re-produced import time failures
* run pytest ... short test 2 failues
* patches syntax bug in pricing module
* run pytest ... 6 failed, 10 passed
* inventory state handling bug fix
* pytest ... 1 failed 15 passed
* final inventory comparison fix and I’m running pytest one more time to confirm everything passes.
* pytest ... 16 passed


```
Summary

Implemented and verified fixes by iteratively running pytest after each change. The suite now passes completely.

### Changes made

1. Fixed a syntax error in [pricing.py](pricing.py)
2. Fixed shared mutable state in [inventory.py](inventory.py) by making stock instance-scoped in `__init__`
3. Fixed fulfillment logic in [inventory.py](inventory.py) by allowing exact-quantity fulfillment with `>=`

### Test runs

1. Initial run showed import-time `SyntaxError` in [pricing.py](pricing.py)
2. After pricing fix, inventory tests failed with state leakage and fulfillment behavior
3. After instance-state fix, one inventory logic failure remained
4. After comparison fix, all tests passed

### Final result

1. pytest status: 16 passed
2. Command used: c:/LabFiles/fde_repo/debugging-refactoring/lab/.venv/Scripts/python.exe -m pytest --tb=short
```


```sh
python.exe -m pytest -v
...
======16 passed in 0.05s ==================
```

# 10.3.3 Audit for Symptom-Levl Fixes




prompt
```python
Lets make sure this is really correct ... please review the state-leak bug fix

The state-leak bug is the lab’s signature symptom-vs.-root-cause trap. The root-cause fix is one line: move _stock from the class level into init so each 
instance gets its own dict. The symptom-level fix is also one line: clear the 
shared dict between tests. Both make the suite green. Only the first one means 
the production code is correct. If you find a symptom fix

Please summarize your results in a couple of lines
```


Results ... Looks Good
```
I’ll quickly inspect the current implementation to verify whether the state leak 
was fixed at the root cause in production code or masked by test-only reset 
logic, then I’ll summarize in two lines.


Read [](file:///c%3A/LabFiles/fde_repo/debugging-refactoring/lab/inventory.py)

Searched for regex `_stock|clear\(|autouse|fixture` (`**/tests/**`), 15 results

Searched for regex `clear\(|Inventory\._stock|_stock\s*=` (`**/*.py`), no results

Reviewed: this is a root-cause fix, not a symptom patch. `_stock` is now instance 
state initialized in `__init__`, so each `Inventory` gets its own dict and state 
cannot leak across instances/tests.  

I found no symptom-level workaround (no shared-dict reset/clear fixture or test 
cleanup); the production behavior is now correct and tests pass for the right 
reason.

```

#  10.3.4. Apply /fix to a Symptom-Level Correction

/fix is a narrower tool than an autonomous loop, which is precisely why it behaves differently on the same bug. A focused /fix call with a specific description of what is structurally wrong (not "make the tests pass" but "move this state so each instance has its own") can produce a root-cause fix where the autonomous loop produced a workaround. This subsection exercises that difference directly.


The key phrasing: you are not asking Copilot to make the tests pass. You are naming the structural problem ("state is being shared across instances") and describing the production consequence ("would cause callers to unexpectedly see each other’s data"). That framing is what pushes the fix toward the root cause — without it, /fix will reproduce the symptom-level workaround the autonomous loop already found. Select the _stock line in inventory.py. In Copilot Chat, run:


highlight the inventory.py class attribute and run the following prompt

prompt
```sh
/fix This class attribute is being shared across instances, which
causes state to leak between tests and would cause production
callers to unexpectedly see each other's data. Move the state so
each Inventory instance has its own stock dict.
```

# 10.3.5 Classify the Bug Type

Bug Types
* **Suitable for autonomous loop:** the fix is mechanical, the test clearly specifies the correct behavior, and the fix does not require judgment beyond what the error message provides. The syntax error fits this category.

* **Suitable with supervision:** autonomous attempts might work but the risk of symptom-level fixes is real. The logic error and the state leak fit here.

* **Not suitable for autonomous loop:** the bug requires judgment, context, or understanding that is not present in the failing test output. The performance issue fits here — no test fails, so the autonomous loop has nothing to optimize against.

Write the Rule
Write one sentence stating the rule you would apply to decide "autonomous loop" vs. "`/fix` in Chat" vs. "fix by hand" for a future failure. The rule should be specific enough that you could apply it on a real failure tomorrow.

The Rule
```text
Use the autonomous loop when a failing test clearly specifies the correct 
behavior and the fix is mechanical, use /fix in Chat when tests point to the 
issue but multiple plausible fixes or code changes require guided reasoning, and fix by hand when the problem lacks a failing test signal or depends on external 
context, performance, or domain judgment.
```