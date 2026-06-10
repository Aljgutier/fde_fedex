const API = "";
let customizationOptions = [];
let pricingTier = "peak";
let menuData = [];

async function loadCustomizations() {
    try {
        const res = await fetch(`${API}/api/customizations`);
        const data = await res.json();
        customizationOptions = data.customizations;
    } catch (err) {
        customizationOptions = [];
    }
}

function getActivePrice(sizeRadio) {
    return pricingTier === "off-peak"
        ? parseFloat(sizeRadio.dataset.offPeakPrice)
        : parseFloat(sizeRadio.dataset.price);
}

function updatePrice(itemId) {
    const sizeRadio = document.querySelector(`input[name="size-${itemId}"]:checked`);
    if (!sizeRadio) return;
    let total = getActivePrice(sizeRadio);
    document.querySelectorAll(`input[name="custom-${itemId}"]:checked`).forEach((cb) => {
        total += parseFloat(cb.dataset.price);
    });
    document.getElementById(`price-${itemId}`).textContent = total.toFixed(2);
}

function renderSizePrice(info) {
    if (pricingTier === "off-peak") {
        return `<span class="size-price-original">$${info.price.toFixed(2)}</span>
                <span class="size-price off-peak-active">$${info.off_peak_price.toFixed(2)}</span>`;
    }
    return `<span class="size-price">$${info.price.toFixed(2)}</span>`;
}

function renderMenu() {
    const container = document.getElementById("menu-list");
    container.innerHTML = "";

    menuData.forEach((item) => {
        const card = document.createElement("div");
        card.className = "menu-card";

        const sizesHtml = Object.entries(item.sizes)
            .map(
                ([size, info]) =>
                    `<label class="size-option">
                        <input type="radio" name="size-${item.id}" value="${size}"
                            data-price="${info.price}"
                            data-off-peak-price="${info.off_peak_price}"
                            ${size === "medium" ? "checked" : ""}>
                        <span class="size-label">${size.charAt(0).toUpperCase() + size.slice(1)}</span>
                        ${renderSizePrice(info)}
                    </label>`
            )
            .join("");

        const customizationsHtml = customizationOptions
            .map(
                (opt) =>
                    `<label class="customization-option">
                        <input type="checkbox" name="custom-${item.id}" value="${opt.id}"
                            data-price="${opt.price}">
                        <span class="custom-label">${opt.name}</span>
                        <span class="custom-price">+$${opt.price.toFixed(2)}</span>
                    </label>`
            )
            .join("");

        const defaultSize = item.sizes.medium || Object.values(item.sizes)[0];
        const defaultPrice = pricingTier === "off-peak"
            ? defaultSize.off_peak_price.toFixed(2)
            : defaultSize.price.toFixed(2);

        card.innerHTML = `
            <h3>${item.name}</h3>
            <p class="description">${item.description}</p>
            <div class="size-selector">
                ${sizesHtml}
            </div>
            ${customizationsHtml ? `<div class="customization-group">${customizationsHtml}</div>` : ""}
            <button class="order-btn" onclick="placeOrder('${item.id}')">
                Order — $<span id="price-${item.id}">${defaultPrice}</span>
            </button>
        `;
        container.appendChild(card);

        card.querySelectorAll(`input[name="size-${item.id}"]`).forEach(
            (radio) => {
                radio.addEventListener("change", () => updatePrice(item.id));
            }
        );
        card.querySelectorAll(`input[name="custom-${item.id}"]`).forEach(
            (cb) => {
                cb.addEventListener("change", () => updatePrice(item.id));
            }
        );
    });
}

async function loadMenu() {
    const container = document.getElementById("menu-list");
    try {
        const res = await fetch(`${API}/api/menu`);
        const data = await res.json();
        menuData = data.items;
        renderMenu();
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load menu.</p>`;
    }
}

let pendingOrder = null;

function placeOrder(itemId) {
    const selectedRadio = document.querySelector(
        `input[name="size-${itemId}"]:checked`
    );
    const size = selectedRadio ? selectedRadio.value : "medium";

    const customizations = [];
    const customizationDetails = [];
    document.querySelectorAll(`input[name="custom-${itemId}"]:checked`).forEach((cb) => {
        customizations.push(cb.value);
        const opt = customizationOptions.find((o) => o.id === cb.value);
        if (opt) customizationDetails.push({ name: opt.name, price: opt.price });
    });

    const card = selectedRadio.closest(".menu-card");
    const drinkName = card.querySelector("h3").textContent;

    pendingOrder = { itemId, size, customizations, drinkName, customizationDetails };
    renderConfirmation();
    document.getElementById("confirm-overlay").classList.remove("hidden");
}

function renderConfirmation() {
    if (!pendingOrder) return;
    const { itemId, size, customizationDetails, drinkName } = pendingOrder;

    const selectedRadio = document.querySelector(
        `input[name="size-${itemId}"]:checked`
    );
    const basePrice = selectedRadio ? getActivePrice(selectedRadio) : 0;
    const total = basePrice + customizationDetails.reduce((sum, c) => sum + c.price, 0);

    const summary = document.getElementById("confirm-summary");
    let html = `<div class="confirm-drink-line">${drinkName} &mdash; ${size.charAt(0).toUpperCase() + size.slice(1)}</div>`;

    if (customizationDetails.length > 0) {
        html += `<div class="confirm-customizations">`;
        customizationDetails.forEach((c) => {
            html += `<div class="confirm-custom-item"><span>${c.name}</span><span>$${c.price.toFixed(2)}</span></div>`;
        });
        html += `</div>`;
    }

    html += `<div class="confirm-total"><span>Total</span><span>$${total.toFixed(2)}</span></div>`;
    summary.innerHTML = html;
}

function closeConfirmation() {
    document.getElementById("confirm-overlay").classList.add("hidden");
    pendingOrder = null;
}

async function submitPendingOrder() {
    if (!pendingOrder) return;
    const { itemId, size, customizations } = pendingOrder;

    try {
        const res = await fetch(`${API}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId, size, customizations, pricing_tier: pricingTier }),
        });
        if (!res.ok) throw new Error("Order failed");

        document.querySelectorAll(`input[name="custom-${itemId}"]`).forEach(
            (cb) => (cb.checked = false)
        );
        updatePrice(itemId);

        closeConfirmation();
        await loadOrders();
        await loadFinancials();
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
        await loadFinancials();
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
        await loadFinancials();
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

function renderReceipt(detail) {
    const sizeName = detail.size.charAt(0).toUpperCase() + detail.size.slice(1);
    let html = `<div class="receipt-line base-item"><span>${detail.item_name} (${sizeName})</span><span>$${detail.base_price.toFixed(2)}</span></div>`;

    if (detail.discount) {
        html += `<div class="receipt-line discount"><span>${detail.discount.label}</span><span>-$${Math.abs(detail.discount.amount).toFixed(2)}</span></div>`;
    }

    detail.customizations.forEach((c) => {
        html += `<div class="receipt-line customization"><span>${c.name}</span><span>$${c.price.toFixed(2)}</span></div>`;
    });

    html += `<div class="receipt-line subtotal"><span>Subtotal</span><span>$${detail.subtotal.toFixed(2)}</span></div>`;
    html += `<div class="receipt-line tax"><span>Tax (8.5%)</span><span>$${detail.tax.toFixed(2)}</span></div>`;
    html += `<div class="receipt-line total"><span>Total</span><span>$${detail.total.toFixed(2)}</span></div>`;

    return `<div class="receipt-panel">${html}</div>`;
}

function toggleReceipt(orderId) {
    const orderEl = document.getElementById(`order-${orderId}`);
    const wrapper = orderEl.querySelector(".receipt-wrapper");
    const btn = orderEl.querySelector(".receipt-btn");
    if (wrapper.style.display === "none") {
        wrapper.style.display = "";
        btn.textContent = "Hide Receipt";
    } else {
        wrapper.style.display = "none";
        btn.textContent = "View Receipt";
    }
}

function renderOrder(order) {
    const div = document.createElement("div");
    div.className = "order-item";
    div.id = `order-${order.order_id}`;
    const cancelBtn =
        order.status === "pending"
            ? `<button class="cancel-btn" onclick="cancelOrder(${order.order_id})">Cancel</button>`
            : "";
    const receiptBtn =
        order.status === "completed" && order.items_detail
            ? `<button class="receipt-btn" onclick="toggleReceipt(${order.order_id})">View Receipt</button>`
            : "";
    const receiptPanel =
        order.status === "completed" && order.items_detail
            ? `<div class="receipt-wrapper" style="display:none">${renderReceipt(order.items_detail)}</div>`
            : "";

    div.innerHTML = `
        <div class="order-row">
            <div class="order-info">
                <span class="order-id">#${order.order_id}</span>
                <span class="order-items">${order.items.join(", ")}</span>
                <span class="order-price">$${order.total_price.toFixed(2)}</span>
            </div>
            <span class="order-status status-${order.status}">${order.status}</span>
            ${getAdvanceButton(order)}
            ${cancelBtn}
            ${receiptBtn}
        </div>
        ${receiptPanel}
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

async function loadFinancials() {
    try {
        const res = await fetch(`${API}/api/financials`);
        const data = await res.json();

        document.getElementById("metric-revenue").textContent = `$${data.total_revenue.toFixed(2)}`;
        document.getElementById("metric-cogs").textContent = `$${data.total_cogs.toFixed(2)}`;
        document.getElementById("metric-margin").textContent = `$${data.margin.toFixed(2)}`;
        document.getElementById("metric-peak-revenue").textContent = `$${data.peak_revenue.toFixed(2)}`;
        document.getElementById("metric-offpeak-revenue").textContent = `$${data.off_peak_revenue.toFixed(2)}`;

        const container = document.getElementById("financials-table-container");
        if (data.orders.length === 0) {
            container.innerHTML = `<p class="empty-state">Place an order to see per-order financials.</p>`;
            return;
        }

        let html = `<table class="financials-table">
            <thead><tr>
                <th>Order</th><th>Drink</th><th>Tier</th><th>Revenue</th><th>COGS</th><th>Margin</th>
            </tr></thead><tbody>`;
        data.orders.forEach((o) => {
            const tierLabel = o.pricing_tier === "off-peak" ? "Off-Peak" : "Peak";
            html += `<tr>
                <td>#${o.order_id}</td>
                <td>${o.drink_name}</td>
                <td>${tierLabel}</td>
                <td>$${o.revenue.toFixed(2)}</td>
                <td>$${o.cogs.toFixed(2)}</td>
                <td class="col-margin">$${o.margin.toFixed(2)}</td>
            </tr>`;
        });
        html += `</tbody></table>`;
        container.innerHTML = html;
    } catch (err) {
        // silently ignore — dashboard is supplementary
    }
}

function onToggleChange() {
    const toggle = document.getElementById("pricing-toggle");
    pricingTier = toggle.checked ? "off-peak" : "peak";

    const label = document.getElementById("tier-label");
    if (pricingTier === "off-peak") {
        label.textContent = "Off-Peak Pricing \u2014 20% Off";
        label.classList.add("off-peak");
    } else {
        label.textContent = "Peak Pricing";
        label.classList.remove("off-peak");
    }

    renderMenu();

    if (pendingOrder) {
        renderConfirmation();
    }
}

// Load on page ready
document.addEventListener("DOMContentLoaded", async () => {
    await loadCustomizations();
    loadMenu();
    loadOrders();
    loadFinancials();

    document.getElementById("pricing-toggle").addEventListener("change", onToggleChange);
    document.getElementById("confirm-order-btn").addEventListener("click", submitPendingOrder);
    document.getElementById("confirm-back-btn").addEventListener("click", closeConfirmation);
    document.getElementById("confirm-overlay").addEventListener("click", (e) => {
        if (e.target === e.currentTarget) closeConfirmation();
    });
});
