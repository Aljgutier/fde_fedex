from dataclasses import asdict

from flask import Flask, jsonify, request

from tickets.store import store


def create_app():
    app = Flask(__name__)

    @app.route("/tickets", methods=["GET"])
    def list_tickets():
        return jsonify([asdict(t) for t in store.list_all()]), 200

    @app.route("/tickets", methods=["POST"])
    def create_ticket():
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        description = data.get("description", "")
        if not title or not isinstance(title, str):
            return jsonify({"error": "title is required"}), 400
        ticket = store.create(title=title, description=description)
        return jsonify(asdict(ticket)), 201

    @app.route("/tickets/<int:ticket_id>", methods=["GET"])
    def get_ticket(ticket_id):
        ticket = store.get(ticket_id)
        if ticket is None:
            return jsonify({"error": "ticket not found"}), 404
        return jsonify(asdict(ticket)), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
