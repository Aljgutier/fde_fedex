const API = "";
const ACTIVE_STATUSES = ["pending", "preparing", "ready"];
const STATUS_LABELS = {
    pending: "Pending",
    preparing: "Preparing",
    ready: "Ready",
    completed: "Completed",
    cancelled: "Cancelled",
};

const STATUS_ACTIONS = {
    pending: [
        { label: "Start Preparing", target: "preparing", className: "advance-btn" },
        { label: "Cancel", target: "cancelled", className: "cancel-btn" },
    ],
    preparing: [{ label: "Mark Ready", target: "ready", className: "advance-btn" }],
    ready: [{ label: "Mark Completed", target: "completed", className: "advance-btn" }],
    completed: [],
    cancelled: [],
};

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

async function updateOrderStatus(orderId, status) {
    try {
        const res = await fetch(`${API}/api/orders/${orderId}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: status }),
        });
        if (!res.ok) {
            let detail = "Status update failed";
            try {
                const errorData = await res.json();
                if (errorData.detail) detail = errorData.detail;
            } catch {
                // Ignore parse issues and use fallback detail.
            }
            throw new Error(detail);
        }
        await loadOrders();
    } catch (err) {
        alert("Failed to update order: " + err.message);
    }
}

function getStatusActions(order) {
    return STATUS_ACTIONS[order.status] || [];
}

function renderOrder(order) {
    const actionsHtml = getStatusActions(order)
        .map(
            (action) =>
                `<button class="${action.className}" onclick="updateOrderStatus(${order.order_id}, '${action.target}')">${action.label}</button>`
        )
        .join("");

    return `
        <div class="order-item">
            <div class="order-info">
                <span class="order-id">#${order.order_id}</span>
                <span class="order-items">${order.items.join(", ")}</span>
                <span class="order-price">$${order.total_price.toFixed(2)}</span>
            </div>
            <div class="order-meta">
                <span class="order-status status-${order.status}">${STATUS_LABELS[order.status] || order.status}</span>
                <div class="order-actions">${actionsHtml}</div>
            </div>
        </div>
    `;
}

function renderOrderGroup(title, orders, emptyMessage) {
    const rows = orders.map(renderOrder).join("");
    const body = rows || `<p class="empty-state">${emptyMessage}</p>`;

    return `
        <section class="orders-group">
            <h3>${title}</h3>
            ${body}
        </section>
    `;
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

        const activeOrders = data.orders.filter((order) =>
            ACTIVE_STATUSES.includes(order.status)
        );
        const completedOrders = data.orders.filter(
            (order) => order.status === "completed"
        );

        container.innerHTML =
            renderOrderGroup(
                "Active",
                activeOrders,
                "No active orders in the queue."
            ) +
            renderOrderGroup(
                "Completed",
                completedOrders,
                "No completed orders yet."
            );
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load orders.</p>`;
    }
}

// Load on page ready
document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    loadOrders();
});
