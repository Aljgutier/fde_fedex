"""
BeanBotics API

FastAPI application serving the BeanBotics coffee ordering system.
"""

from dataclasses import asdict
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from backend.services.menu import MenuService
from backend.services.orders import OrderService


app = FastAPI(title="BeanBotics", version="0.1.0")

# Initialize services
menu_service = MenuService()
order_service = OrderService(menu_service)

# Serve frontend static files
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


# --- Request Models ---

class OrderRequest(BaseModel):
    item_id: str
    size: str


class StatusUpdateRequest(BaseModel):
    status: str


# --- Routes ---

@app.get("/")
async def root():
    return FileResponse(str(frontend_dir / "index.html"))


@app.get("/api/menu")
async def get_menu():
    items = menu_service.get_all_items()
    return {"items": [asdict(item) for item in items]}


@app.post("/api/orders")
async def place_order(request: OrderRequest):
    order = order_service.place_order(request.item_id, request.size)
    if not order:
        raise HTTPException(status_code=400, detail="Invalid item or size")
    return {"order": asdict(order)}


@app.get("/api/orders")
async def list_orders():
    orders = order_service.get_all_orders()
    return {"orders": [asdict(o) for o in orders]}


@app.patch("/api/orders/{order_id}/status")
async def update_order_status(order_id: int, request: StatusUpdateRequest):
    outcome, order, message = order_service.update_order_status(order_id, request.status)

    if outcome == "not_found":
        raise HTTPException(status_code=404, detail=message)
    if outcome == "invalid_status":
        raise HTTPException(status_code=400, detail=message)
    if outcome == "invalid_transition":
        raise HTTPException(status_code=409, detail=message)

    return {"order": asdict(order)}


@app.delete("/api/orders/{order_id}")
async def cancel_order(order_id: int):
    outcome, _, message = order_service.update_order_status(order_id, "cancelled")
    if outcome == "not_found":
        raise HTTPException(status_code=404, detail=message)
    if outcome == "invalid_transition":
        raise HTTPException(status_code=409, detail=message)
    return {"message": f"Order {order_id} cancelled"}
