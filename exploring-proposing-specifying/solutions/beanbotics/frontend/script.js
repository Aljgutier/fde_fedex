const API = "";

async function loadMenu() {
    const container = document.getElementById("menu-list");
    try {
        const res = await fetch(`${API}/api/menu`);
        const data = await res.json();
        container.innerHTML = "";

        data.items.forEach((item) => {
            const card = document.createElement("div");
            card.className = "menu-card";

            const sizesHtml = Object.entries(item.sizes)
                .map(
                    ([size, info]) =>
                        `<label class="size-option">
                            <input type="radio" name="size-${item.id}" value="${size}"
                                data-price="${info.price}"
                                ${size === "medium" ? "checked" : ""}>
                            <span class="size-label">${size.charAt(0).toUpperCase() + size.slice(1)}</span>
                            <span class="size-price">$${info.price.toFixed(2)}</span>
                        </label>`
                )
                .join("");

            const defaultPrice = item.sizes.medium
                ? item.sizes.medium.price.toFixed(2)
                : Object.values(item.sizes)[0].price.toFixed(2);

            card.innerHTML = `
                <h3>${item.name}</h3>
                <p class="description">${item.description}</p>
                <div class="size-selector">
                    ${sizesHtml}
                </div>
                <button class="order-btn" onclick="placeOrder('${item.id}')">
                    Order — $<span id="price-${item.id}">${defaultPrice}</span>
                </button>
            `;
            container.appendChild(card);

            // Update displayed price when size selection changes
            card.querySelectorAll(`input[name="size-${item.id}"]`).forEach(
                (radio) => {
                    radio.addEventListener("change", () => {
                        const priceSpan = document.getElementById(
                            `price-${item.id}`
                        );
                        priceSpan.textContent =
                            parseFloat(radio.dataset.price).toFixed(2);
                    });
                }
            );
        });
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load menu.</p>`;
    }
}

async function placeOrder(itemId) {
    const selectedRadio = document.querySelector(
        `input[name="size-${itemId}"]:checked`
    );
    const size = selectedRadio ? selectedRadio.value : "medium";

    try {
        const res = await fetch(`${API}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId, size: size }),
        });
        if (!res.ok) throw new Error("Order failed");
        await loadOrders();
    } catch (err) {
        alert("Failed to place order: " + err.message);
    }
}

async function advanceOrder(orderId, nextStatus) {
    try {
        const res = await fetch(`${API}/api/orders/${orderId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: nextStatus }),
        });
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Update failed");
        }
        await loadOrders();
    } catch (err) {
        alert("Failed to update order: " + err.message);
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

function getAdvanceButton(order) {
    const nextMap = {
        pending: { status: "preparing", label: "Start Preparing" },
        preparing: { status: "ready", label: "Mark Ready" },
        ready: { status: "completed", label: "Complete" },
    };
    const next = nextMap[order.status];
    if (!next) return "";
    return `<button class="advance-btn" onclick="advanceOrder(${order.order_id}, '${next.status}')">${next.label}</button>`;
}

function renderOrder(order) {
    const div = document.createElement("div");
    div.className = "order-item";
    const cancelBtn =
        order.status === "pending"
            ? `<button class="cancel-btn" onclick="cancelOrder(${order.order_id})">Cancel</button>`
            : "";
    div.innerHTML = `
        <div class="order-info">
            <span class="order-id">#${order.order_id}</span>
            <span class="order-items">${order.items.join(", ")}</span>
            <span class="order-price">$${order.total_price.toFixed(2)}</span>
        </div>
        <span class="order-status status-${order.status}">${order.status}</span>
        ${getAdvanceButton(order)}
        ${cancelBtn}
    `;
    return div;
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

        const active = data.orders.filter(
            (o) => o.status === "pending" || o.status === "preparing" || o.status === "ready"
        );
        const completed = data.orders.filter((o) => o.status === "completed");

        container.innerHTML = "";

        if (active.length > 0) {
            const heading = document.createElement("p");
            heading.className = "order-group-heading";
            heading.textContent = "Active Orders";
            container.appendChild(heading);
            active.forEach((order) => container.appendChild(renderOrder(order)));
        }

        if (completed.length > 0) {
            const heading = document.createElement("p");
            heading.className = "order-group-heading";
            heading.textContent = "Completed";
            container.appendChild(heading);
            completed.forEach((order) => container.appendChild(renderOrder(order)));
        }
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load orders.</p>`;
    }
}

// Load on page ready
document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    loadOrders();
});
