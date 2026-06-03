# Ticket Tracker

A minimal Flask-based support ticket tracker. This repository is the starter for a cloud agent lab. You will push it to your own GitHub repository, open an issue describing a feature, assign the issue to GitHub Copilot, and then observe the cloud agent work through the implementation.

## Existing API

| Method | Path                 | Description                |
|--------|----------------------|----------------------------|
| GET    | `/tickets`           | List all tickets           |
| POST   | `/tickets`           | Create a new ticket        |
| GET    | `/tickets/<id>`      | Retrieve a single ticket   |

## Ticket Shape

```json
{
  "id": 1,
  "title": "Page loads slowly",
  "description": "Dashboard takes 15s+ on first load",
  "status": "open",
  "created_at": "2026-01-15T10:00:00Z"
}
```

Valid `status` values are `open`, `in_progress`, `resolved`, and `closed`. Tickets are created with `status: open`.

## Running

```bash
uv venv --seed --python=3.13
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m tickets.app
pytest
```

## Files for the Lab

- `ISSUE_CORE.md` — the feature brief you will paste into a GitHub issue for the Core task
- `ISSUE_AMBIGUOUS.md` — the deliberately under-specified brief for Challenge 2
- `ISSUE_TEMPLATE.md` — the template that describes what a well-scoped issue for the cloud agent looks like
