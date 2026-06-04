# Solution Reference

A worked reference implementation of the Core issue. Compare against the PR the cloud agent produces to evaluate its output; do not copy from here directly.

## What Changed

- `tickets/models.py` — added `updated_at` to the `Ticket` dataclass.
- `tickets/store.py` — added an `update_status` method; new tickets now populate `updated_at` on creation.
- `tickets/app.py` — added `PATCH /tickets/<id>/status` with validation for missing body, missing field, and invalid values.
- `tests/test_tickets.py` — added tests for success, 404, missing body, missing field, and each invalid-status path.

## Running

```bash
python -m tickets.app
pytest
```
