from flask import Flask, jsonify, request

from storage import TaskStore

app = Flask(__name__)
store = TaskStore()


@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(store.list_all()), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    task = store.create(
        title=data.get("title", ""),
        status=data.get("status", "pending"),
    )
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
