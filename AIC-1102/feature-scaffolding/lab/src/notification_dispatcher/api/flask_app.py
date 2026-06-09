from __future__ import annotations

from dataclasses import asdict
from typing import Any

from flask import Flask, current_app, request

from notification_dispatcher.application.dto import (
    CreateNotificationCommand,
    NotificationView,
)
from notification_dispatcher.application.services.dispatch_service import DispatchService
from notification_dispatcher.application.services.query_service import QueryService


def create_flask_app(
    dispatch_service: DispatchService | None = None,
    query_service: QueryService | None = None,
) -> Flask:
    app = Flask(__name__)
    app.config["dispatch_service"] = dispatch_service
    app.config["query_service"] = query_service
    register_routes(app)
    return app


def register_routes(app: Flask) -> None:
    app.add_url_rule("/notifications", view_func=post_notifications, methods=["POST"])
    app.add_url_rule("/notifications", view_func=get_notifications, methods=["GET"])
    app.add_url_rule(
        "/notifications/<notification_id>",
        view_func=get_notification,
        methods=["GET"],
    )


def post_notifications() -> tuple[dict[str, Any], int]:
    dispatch_service: DispatchService | None = current_app.config.get("dispatch_service")
    if dispatch_service is None:
        return {"error": "dispatch service is not configured"}, 500

    payload = request.get_json(silent=True) or {}
    cmd = CreateNotificationCommand(
        recipient=str(payload.get("recipient", "")),
        channels=list(payload.get("channels", [])),
        subject=str(payload.get("subject", "")),
        body=str(payload.get("body", "")),
    )
    try:
        view = dispatch_service.create_and_dispatch(cmd=cmd)
    except ValueError as exc:
        return {"error": str(exc)}, 400
    return _view_to_dict(view), 201


def get_notification(notification_id: str) -> tuple[dict[str, Any], int]:
    query_service: QueryService | None = current_app.config.get("query_service")
    if query_service is None:
        return {"error": "query service is not configured"}, 500

    view = query_service.get_notification(notification_id)
    if view is None:
        return {"error": "notification not found"}, 404
    return _view_to_dict(view), 200


def get_notifications() -> tuple[dict[str, Any], int]:
    query_service: QueryService | None = current_app.config.get("query_service")
    if query_service is None:
        return {"error": "query service is not configured"}, 500

    recipient = request.args.get("recipient", default="", type=str)
    if not recipient:
        return {"error": "recipient query parameter is required"}, 400

    views = query_service.list_for_recipient(recipient)
    return {"items": [_view_to_dict(v) for v in views]}, 200


def _view_to_dict(view: NotificationView) -> dict[str, Any]:
    data = asdict(view)
    data["created_at"] = view.created_at.isoformat()
    data["updated_at"] = view.updated_at.isoformat()
    return data
