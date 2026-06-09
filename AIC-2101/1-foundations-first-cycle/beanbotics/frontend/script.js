const API = "";
const SIZE_ORDER = ["small", "medium", "large"];
let menuItemsById = {};

function formatSizeLabel(size) {
    return size.charAt(0).toUpperCase() + size.slice(1);
}

function getOrderedSizes(item) {
    const available = Object.keys(item.sizes || {});
    return available.sort((a, b) => {
        const aIdx = SIZE_ORDER.indexOf(a);
        const bIdx = SIZE_ORDER.indexOf(b);
        const safeA = aIdx === -1 ? SIZE_ORDER.length : aIdx;
        const safeB = bIdx === -1 ? SIZE_ORDER.length : bIdx;
        return safeA - safeB;
    });
}

function updateCardPrice(itemId) {
    const item = menuItemsById[itemId];
    if (!item) return;

    const select = document.getElementById(`size-${itemId}`);
    const priceEl = document.getElementById(`price-${itemId}`);
    const button = document.getElementById(`order-${itemId}`);
    if (!select || !priceEl || !button) return;

    const selectedSize = select.value;
    const selectedSizeData = item.sizes?.[selectedSize];
    if (!selectedSizeData) {
        priceEl.textContent = "Price unavailable";
        button.disabled = true;
        return;
    }

    priceEl.textContent = `$${selectedSizeData.price.toFixed(2)}`;
    button.disabled = false;
    button.textContent = `Order (${formatSizeLabel(selectedSize)})`;
}

async function loadMenu() {
    const container = document.getElementById("menu-list");
    try {
        const res = await fetch(`${API}/api/menu`);
        const data = await res.json();
        container.innerHTML = "";
        menuItemsById = {};

        data.items.forEach((item) => {
            menuItemsById[item.id] = item;
            const sizes = getOrderedSizes(item);
            const defaultSize = sizes[0];

            const options = sizes
                .map((size) => `<option value="${size}">${formatSizeLabel(size)}</option>`)
                .join("");

            const card = document.createElement("div");
            card.className = "menu-card";
            card.innerHTML = `
                <h3>${item.name}</h3>
                <p class="description">${item.description}</p>
                <label class="size-label" for="size-${item.id}">Size</label>
                <select id="size-${item.id}" class="size-select" onchange="updateCardPrice('${item.id}')">
                    ${options}
                </select>
                <p class="price" id="price-${item.id}">--</p>
                <button id="order-${item.id}" class="order-btn" onclick="placeOrder('${item.id}')" ${defaultSize ? "" : "disabled"}>
                    Order
                </button>
            `;
            container.appendChild(card);
            updateCardPrice(item.id);
        });
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load menu.</p>`;
    }
}

async function placeOrder(itemId) {
    const sizeSelect = document.getElementById(`size-${itemId}`);
    const selectedSize = sizeSelect?.value;
    if (!selectedSize) {
        alert("Please choose a size before ordering.");
        return;
    }

    try {
        const res = await fetch(`${API}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId, size: selectedSize }),
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
