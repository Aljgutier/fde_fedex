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

from backend.models import OrderStatus, CUSTOMIZATIONS
from backend.services.menu import MenuService
from backend.services.orders import OrderService
from backend.services.ingredients import IngredientService


app = FastAPI(title="BeanBotics", version="0.1.0")

# Initialize services
ingredient_service = IngredientService()
menu_service = MenuService()
menu_service.validate_recipes(set(ingredient_service.ingredients.keys()))
order_service = OrderService(menu_service, ingredient_service)

# Serve frontend static files
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


# --- Request Models ---

class OrderRequest(BaseModel):
    item_id: str
    size: str
    customizations: list[str] = []


class StatusUpdateRequest(BaseModel):
    status: OrderStatus


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
    order = order_service.place_order(request.item_id, request.size, request.customizations)
    if not order:
        raise HTTPException(status_code=400, detail="Invalid item, size, or customization")
    return {"order": asdict(order)}


@app.get("/api/customizations")
async def get_customizations():
    return {
        "customizations": [
            {"id": cid, "name": info["name"], "price": info["price"]}
            for cid, info in CUSTOMIZATIONS.items()
        ]
    }


@app.get("/api/orders")
async def list_orders():
    orders = order_service.get_all_orders()
    return {"orders": [asdict(o) for o in orders]}


@app.patch("/api/orders/{order_id}")
async def update_order_status(order_id: int, request: StatusUpdateRequest):
    try:
        order = order_service.update_order_status(order_id, request.status)
        return {"order": asdict(order)}
    except ValueError as e:
        msg = str(e)
        if "not found" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@app.get("/api/financials")
async def get_financials():
    orders = order_service.get_all_orders()
    total_revenue = sum(o.total_price for o in orders)
    total_cogs = sum(o.cogs for o in orders if o.cogs is not None)
    margin = round(total_revenue - total_cogs, 2)
    order_breakdown = []
    for o in orders:
        cogs = o.cogs or 0
        order_breakdown.append({
            "order_id": o.order_id,
            "drink_name": o.items[0] if o.items else "",
            "revenue": o.total_price,
            "cogs": cogs,
            "margin": round(o.total_price - cogs, 2),
        })
    return {
        "total_revenue": round(total_revenue, 2),
        "total_cogs": round(total_cogs, 2),
        "margin": margin,
        "orders": order_breakdown,
    }


@app.delete("/api/orders/{order_id}")
async def cancel_order(order_id: int):
    success = order_service.cancel_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found or cannot be cancelled")
    return {"message": f"Order {order_id} cancelled"}
