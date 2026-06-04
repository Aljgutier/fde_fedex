# Solution Reference

Completed tests for every module and a reference `testing.instructions.md` for Challenge 2.

## Contents

```
tests/
├── test_cart.py          # completed — covers set_quantity, lines, subtotal, is_empty, add validation
├── test_discounts.py     # completed — covers all three discount functions and every error path
├── test_tax.py           # full coverage — rate_for_state, calculate_tax, is_tax_exempt
└── test_shipping.py      # full coverage — base_rate, expedited_surcharge, estimate
.github/
└── instructions/
    └── testing.instructions.md  # Challenge 2 reference
```

## How to Use This

Do not copy these files into the starter to skip the Core exercise. Compare them against Copilot's output *after* your Core run:

- How does Copilot's generated coverage compare to the reference in breadth?
- Which error paths did Copilot cover, and which did it skip?
- Did Copilot match the reference style (parametrized, grouped into classes, `with pytest.raises` for errors)?

The `testing.instructions.md` in this folder is what you might author for Challenge 2 — compare against your own version, not as an answer key.
