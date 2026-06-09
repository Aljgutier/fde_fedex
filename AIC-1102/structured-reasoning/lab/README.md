# Messy Project

A small application organized in a conventional `src/` layout, with source, tests, config, scripts, and data separated cleanly.

## Project Layout

```
messy_project/
├── README.md
├── src/
│   └── messy_project/
│       ├── __init__.py
│       ├── main.py
│       ├── helpers.py
│       └── old_utils.py
├── config/
│   └── app.yaml
├── data/
│   ├── sample.json
│   └── data_loader.yaml
├── scripts/
│   ├── deploy.sh
│   ├── deploy_helpers.py
│   └── run_tests.sh
├── conftest.py
└── tests/
    ├── __init__.py
    ├── test_main.py
    └── test_helpers.py
```

## Running

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src python -m messy_project.main
pytest
```

Both commands should succeed from the project root.
