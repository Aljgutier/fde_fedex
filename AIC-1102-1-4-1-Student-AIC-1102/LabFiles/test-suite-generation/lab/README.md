# Orders Library — Test Generation Lab

A small order-processing library with *deliberately partial* test coverage. You will use Copilot to identify the coverage gaps, generate tests for the untested modules, and evaluate the quality of what it produced.

## Layout

```
.
├── orders/
│   ├── money.py          # decimal/currency helpers — reference style
│   ├── cart.py           # cart operations
│   ├── discounts.py      # discount calculations
│   ├── tax.py            # tax computation
│   └── shipping.py       # shipping cost estimation
├── tests/
│   ├── test_money.py
│   ├── test_cart.py
│   └── test_discounts.py
├── COVERAGE_BASELINE.md  # ground truth — do not open until Step 2
└── requirements.txt
```

## Running the Existing Tests

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Some modules have tests and some do not. Confirm the existing suite passes before generating new tests against it.

## Important

`COVERAGE_BASELINE.md` contains the authoritative statement of what is tested and what is not. Do not open it until Core Step 2 — the first step of the lab is observing what Copilot reports about coverage *without* having read the baseline yourself.
