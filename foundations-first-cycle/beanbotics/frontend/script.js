const API = "";

async function loadMenu() {
    const container = document.getElementById("menu-list");
    try {
        const res = await fetch(`${API}/api/menu`);
        const data = await res.json();
        container.innerHTML = "";

        data.items.forEach((item) => {
            const mediumPrice = item.sizes.medium
                ? item.sizes.medium.price.toFixed(2)
                : "—";

            const card = document.createElement("div");
            card.className = "menu-card";
            card.innerHTML = `
                <h3>${item.name}</h3>
                <p class="description">${item.description}</p>
                <p class="price">From $${mediumPrice}</p>
                <button class="order-btn" onclick="placeOrder('${item.id}')">
                    Order (Medium)
                </button>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load menu.</p>`;
    }
}

async function placeOrder(itemId) {
    try {
        const res = await fetch(`${API}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId, size: "medium" }),
        });
        if (!res.ok) throw new Error("Order failed");
        await loadOrders();
    } catch (err) {
        alert("Failed to place order: " + err.message);
    }
}

async function cancelOrder(orderId) {
    try {
        const res = await fetch(`${API}/api/orders/${orderId}`, {
            method: "DELETE",
        });
        if (!res.ok) throw new Error("Cancel failed");
        await loadOrders();
    } catch (err) {
        alert("Failed to cancel order: " + err.message);
    }
}

async function loadOrders() {
    const container = document.getElementById("orders-list");
    try {
        const res = await fetch(`${API}/api/orders`);
        const data = await res.json();

        if (data.orders.length === 0) {
            container.innerHTML = `<p class="empty-state">No orders yet. Pick a drink from the menu!</p>`;
            return;
        }

        container.innerHTML = "";
        data.orders.forEach((order) => {
            const div = document.createElement("div");
            div.className = "order-item";
            div.innerHTML = `
                <div class="order-info">
                    <span class="order-id">#${order.order_id}</span>
                    <span class="order-items">${order.items.join(", ")}</span>
                    <span class="order-price">$${order.total_price.toFixed(2)}</span>
                </div>
                <span class="order-status">${order.status}</span>
                ${
                    order.status === "pending"
                        ? `<button class="cancel-btn" onclick="cancelOrder(${order.order_id})">Cancel</button>`
                        : ""
                }
            `;
            container.appendChild(div);
        });
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load orders.</p>`;
    }
}

// Load on page ready
document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    loadOrders();
});
