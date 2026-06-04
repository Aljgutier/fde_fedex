# Coverage Baseline — Ground Truth

This is the authoritative statement of what is tested in the starter. Use it in Core Step 2 to evaluate the coverage assessment Copilot produces via `#codebase`.

## Per-Module State

| Module                  | State                 | What is covered                                          | What is missing                                         |
|-------------------------|-----------------------|----------------------------------------------------------|----------------------------------------------------------|
| `orders/money.py`       | Fully tested          | All three functions (`round_cents`, `format_usd`, `parse_amount`) with parametrized cases, error paths, and edge cases. | Nothing. This is the reference for style. |
| `orders/cart.py`        | Partially tested      | `add` (new line and incrementing existing) and `remove` (present and absent sku). | `set_quantity` (all paths), `lines`, `subtotal`, `is_empty`; `add` quantity validation (`quantity < 1`). |
| `orders/discounts.py`   | Partially tested      | One happy-path test for `percentage_discount`.            | Every error path on `percentage_discount` (negative, > 100), all of `fixed_amount_discount`, all of `bulk_discount` and its tiers. |
| `orders/tax.py`         | **Untested**          | Nothing.                                                 | Everything: `rate_for_state`, `calculate_tax` (general, exempt, unknown state), `is_tax_exempt`. |
| `orders/shipping.py`    | **Untested**          | Nothing.                                                 | Everything: `base_rate`, `expedited_surcharge`, `estimate` (free threshold, expedited flag, the interaction between them). |

## Test Count by Module

At the start of the lab:

| Module                  | Tests in starter |
|-------------------------|------------------|
| `orders/money.py`       | 16               |
| `orders/cart.py`        | 4                |
| `orders/discounts.py`   | 1                |
| `orders/tax.py`         | 0                |
| `orders/shipping.py`    | 0                |

Total: 21.

## Reference Style

`tests/test_money.py` demonstrates the conventions you should expect Copilot to match when it generates new tests:

- pytest (not `unittest`). Function-based or test-class-based; no `TestCase` subclasses.
- Test classes group tests for one function (e.g., `class TestRoundCents:`).
- Parametrized tests (`@pytest.mark.parametrize`) wherever the test varies input values on the same assertion shape.
- Error paths use `with pytest.raises(...)`.
- Edge cases are explicit: zero, negative, boundary values.
- No mocking (the library has no external dependencies).
