from flask import Flask, jsonify, request

from storage import TaskStore

app = Flask(__name__)
store = TaskStore()
VALID_STATUSES = ["pending", "in_progress", "done"]
ALLOWED_STATUSES = set(VALID_STATUSES)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def invalid_status_response():
    return (
        jsonify(
            {
                "error": "status must be one of: pending, in_progress, done",
                "valid_statuses": VALID_STATUSES,
            }
        ),
        422,
    )


def validate_task_payload(data, require_title=False, require_any=False):
    if not isinstance(data, dict):
        return "invalid JSON body", 400

    has_title = "title" in data
    has_status = "status" in data

    if require_any and not (has_title or has_status):
        return "at least one of title or status is required", 400

    if require_title and not has_title:
        return "title is required", 400

    if has_title:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return "title must be a non-empty string", 400

    if has_status and data["status"] not in ALLOWED_STATUSES:
        return "status must be one of: pending, in_progress, done", 422

    return None, None


@app.route("/tasks", methods=["GET"])
def list_tasks():
    status = request.args.get("status")
    tasks = store.list_all(status=status) if status is not None else store.list_all()
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    error, status_code = validate_task_payload(data, require_title=True)
    if error:
        if status_code == 422:
            return invalid_status_response()
        return error_response(error, status_code)

    task = store.create(
        title=data["title"],
        status=data.get("status", "pending"),
    )
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = store.get(task_id)
    if task is None:
        return error_response("task not found", 404)
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if store.get(task_id) is None:
        return error_response("task not found", 404)

    data = request.get_json(silent=True) or {}
    error, status_code = validate_task_payload(data, require_any=True)
    if error:
        if status_code == 422:
            return invalid_status_response()
        return error_response(error, status_code)

    updates = {}
    if "title" in data:
        updates["title"] = data["title"]
    if "status" in data:
        updates["status"] = data["status"]

    task = store.update(task_id, updates)
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = store.delete(task_id)
    if not deleted:
        return error_response("task not found", 404)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, port=5000)
