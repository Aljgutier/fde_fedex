# Messy Project

A small application that has grown organically and now has a layout problem: source, tests, config, scripts, and data are all at the top level or nearly so, and some filenames collide semantically across directories.

This repository is the *starting* state for a structural refactor. In this lab you will plan the move to a conventional `src/` layout and execute it with Copilot's help.

## Starting Layout

```
messy_project/
├── main.py                 # entry point
├── helpers.py              # shared helpers for the module
├── old_utils.py            # legacy utilities - read me carefully
├── config.yaml             # application configuration
├── test_main.py            # a test file at the root
├── README.md
├── data/
│   ├── sample.json
│   └── config.yaml         # data loader settings (distinct from the app config)
├── scripts/
│   ├── deploy.sh
│   ├── helpers.py          # deployment helpers (distinct from the module helpers)
│   └── run_tests.sh
└── tests/
    └── test_helpers.py
```

## Running

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
pytest
```

Both should succeed on the starter. Your job is to plan and execute a restructure that leaves them still succeeding.

## Known Traps

Before you touch anything, be aware:

1. Two files named `config.yaml` exist in different directories. They are **not** duplicates.
2. Two files named `helpers.py` exist in different directories. They are **not** duplicates.
3. `old_utils.py` looks deprecated. Before deciding, check whether anything imports from it.
4. The `README.md` description above is what the project *intends* to be, not a guarantee of what it *is*.
