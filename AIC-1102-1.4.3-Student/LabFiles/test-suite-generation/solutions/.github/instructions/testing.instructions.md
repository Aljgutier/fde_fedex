---
applyTo: "tests/**/*.py"
---

# Testing Conventions

These rules apply to every test file in this repository.

## Framework

- Use `pytest`. Do not use `unittest.TestCase`, `nose`, or `doctest` for new tests.
- Prefer function-based tests or lightweight test classes (`class TestFoo:`). Do not inherit from `TestCase`.
- Group tests for a single function or method into one `TestXxx` class. One class per function under test.

## Fixtures

- Define fixtures at the top of the test module. Promote fixtures to `conftest.py` only when two or more test files share them.
- Fixtures that produce objects return the object directly. Do not yield unless teardown is needed.
- Do not use `autouse=True` fixtures to hide state bugs. If a test needs fresh state, construct fresh objects inside each test.

## Parametrization

- Use `@pytest.mark.parametrize` when the same assertion shape applies to multiple input-output pairs. Do not write six nearly-identical tests that parametrize would collapse.
- Parameter rows should be readable as a truth table. Keep the id derivation automatic (do not hand-name `ids=[...]` unless the default ids are unreadable).
- Split into separate parametrized tests when the assertion shape differs (for example, error paths in one parametrize, success paths in another).

## Assertions

- Assert specific values, not truthiness. `assert result == Decimal("5.00")` beats `assert result`.
- For exceptions, use `with pytest.raises(ExceptionType):`. Assert the exception type specifically; do not catch with `Exception` unless the test explicitly cares about the general case.
- Avoid asserting on exception messages unless the message is part of the API contract.

## Coverage Requirements

Every new test file must cover:

- **The success path** for each public function.
- **Every documented error path** (every `raise` in the source with a distinct `ExceptionType`).
- **Boundary values** — for numeric inputs, at minimum: zero, one, and the values at either side of any threshold in the implementation.
- **Every branch** in the implementation that a test can reach without mocking.

## Style

- Test name pattern: `test_<scenario>` for function-based tests, or `test_<scenario>` inside a `TestXxx` class. Scenario should describe the *expected outcome*, not the input ("test_negative_quantity_raises", not "test_neg_qty").
- One behavior per test. If the test contains more than ~3 assertions, split it.
- Do not import the module under test using wildcard imports.

## What NOT to Do

- No mocking for this repository's tests. Every module's dependencies are either in-memory (like `cart`) or pure functions (like `discounts`); there is no external service, database, or clock to mock.
- No time-dependent assertions (`assert t1 - t0 < 0.1`). Tests must be deterministic across machines.
- No file-system writes from tests. If a test needs a fixture file, store it under `tests/fixtures/` and read it read-only.
- No testing private methods (names starting with `_`). Test through the public API.
- No tests that pass regardless of the implementation ("does not raise" is only a valid assertion for error-path tests; otherwise assert on the return value).
