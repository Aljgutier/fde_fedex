const API = "";

const CUSTOMIZATION_PRICES = {
    extra_shot: 0.75,
    milk_alternative: 0.60,
    whipped_cream: 0.50,
};

let menuItemsById = {};
let pendingReview = null;

function getSelectedSizeInfo(itemId) {
    const selectedRadio = document.querySelector(`input[name="size-${itemId}"]:checked`);
    return {
        size: selectedRadio ? selectedRadio.value : "medium",
        price: selectedRadio ? parseFloat(selectedRadio.dataset.price) : 0,
    };
}

function getSelectedCustomizations(itemId) {
    const extraShot = document.getElementById(`extra-shot-${itemId}`)?.checked ?? false;
    const whippedCream = document.getElementById(`whipped-cream-${itemId}`)?.checked ?? false;
    const milkAlternative =
        document.querySelector(`input[name="milk-${itemId}"]:checked`)?.value || "none";

    return {
        extra_shot: extraShot,
        milk_alternative: milkAlternative,
        whipped_cream: whippedCream,
    };
}

function getCustomizationLineItems(customizations) {
    const lineItems = [];
    if (customizations.extra_shot) {
        lineItems.push({ label: "Extra shot", price: CUSTOMIZATION_PRICES.extra_shot });
    }
    if (customizations.milk_alternative !== "none") {
        const milkName =
            customizations.milk_alternative.charAt(0).toUpperCase() +
            customizations.milk_alternative.slice(1);
        lineItems.push({ label: `${milkName} milk`, price: CUSTOMIZATION_PRICES.milk_alternative });
    }
    if (customizations.whipped_cream) {
        lineItems.push({ label: "Whipped cream", price: CUSTOMIZATION_PRICES.whipped_cream });
    }
    return lineItems;
}

function calculateTotal(basePrice, customizations) {
    let total = basePrice;
    getCustomizationLineItems(customizations).forEach((item) => {
        total += item.price;
    });
    return total;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function updateCardPrice(itemId) {
    const priceSpan = document.getElementById(`price-${itemId}`);
    const sizeInfo = getSelectedSizeInfo(itemId);
    const customizations = getSelectedCustomizations(itemId);
    const total = calculateTotal(sizeInfo.price, customizations);
    if (priceSpan) {
        priceSpan.textContent = total.toFixed(2);
    }
}

function formatCustomizationSummary(customizations) {
    if (!customizations) {
        return "";
    }

    const labels = [];
    if (customizations.extra_shot) {
        labels.push("Extra shot");
    }
    if (customizations.milk_alternative && customizations.milk_alternative !== "none") {
        labels.push(`${customizations.milk_alternative.charAt(0).toUpperCase()}${customizations.milk_alternative.slice(1)} milk`);
    }
    if (customizations.whipped_cream) {
        labels.push("Whipped cream");
    }

    if (labels.length === 0) {
        return "";
    }

    return `
        <div class="order-customizations">
            ${labels.map((label) => `<span class="customization-chip">${label}</span>`).join("")}
        </div>
    `;
}

async function loadMenu() {
    const container = document.getElementById("menu-list");
    try {
        const res = await fetch(`${API}/api/menu`);
        const data = await res.json();
        container.innerHTML = "";
        menuItemsById = Object.fromEntries(data.items.map((item) => [item.id, item]));

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
                <div class="customization-selector">
                    <label class="customization-option">
                        <input type="checkbox" id="extra-shot-${item.id}">
                        Extra espresso shot (+$0.75)
                    </label>
                    <div class="milk-alternatives">
                        <span class="customization-label">Milk alternative (+$0.60):</span>
                        <label><input type="radio" name="milk-${item.id}" value="none" checked> None</label>
                        <label><input type="radio" name="milk-${item.id}" value="oat"> Oat</label>
                        <label><input type="radio" name="milk-${item.id}" value="almond"> Almond</label>
                        <label><input type="radio" name="milk-${item.id}" value="soy"> Soy</label>
                    </div>
                    <label class="customization-option">
                        <input type="checkbox" id="whipped-cream-${item.id}">
                        Whipped cream (+$0.50)
                    </label>
                </div>
                <button class="order-btn" onclick="startOrderReview('${item.id}')">
                    Order - $<span id="price-${item.id}">${defaultPrice}</span>
                </button>
            `;
            container.appendChild(card);

            // Update displayed price when size selection changes
            card.querySelectorAll(`input[name="size-${item.id}"]`).forEach(
                (radio) => {
                    radio.addEventListener("change", () => {
                        updateCardPrice(item.id);
                    });
                }
            );

            card.querySelectorAll(`#extra-shot-${item.id}, #whipped-cream-${item.id}, input[name="milk-${item.id}"]`).forEach(
                (control) => {
                    control.addEventListener("change", () => updateCardPrice(item.id));
                }
            );
        });
    } catch (err) {
        container.innerHTML = `<p class="empty-state">Failed to load menu.</p>`;
    }
}

function renderReviewSummary(review) {
    const lines = [
        `<li><span>${escapeHtml(review.displayName)}</span><span>$${review.basePrice.toFixed(2)}</span></li>`,
        ...review.customizationItems.map(
            (item) =>
                `<li><span>${escapeHtml(item.label)}</span><span>$${item.price.toFixed(2)}</span></li>`
        ),
    ].join("");

    return `
        <p class="review-subtitle">Review Your Order</p>
        <p class="review-item-name">${escapeHtml(review.displayName)}</p>
        <ul class="review-line-items">
            ${lines}
        </ul>
        <p class="review-total">Pre-tax total <strong>$${review.subtotal.toFixed(2)}</strong></p>
    `;
}

function closeReviewModal() {
    const modal = document.getElementById("review-modal");
    const body = document.getElementById("review-body");
    if (modal) {
        modal.classList.add("hidden");
    }
    if (body) {
        body.innerHTML = "";
    }
    pendingReview = null;
}

function startOrderReview(itemId) {
    const item = menuItemsById[itemId];
    if (!item) {
        alert("Menu item no longer available.");
        return;
    }

    const sizeInfo = getSelectedSizeInfo(itemId);
    const customizations = getSelectedCustomizations(itemId);
    const customizationItems = getCustomizationLineItems(customizations);
    const subtotal = calculateTotal(sizeInfo.price, customizations);

    pendingReview = {
        itemId,
        payload: {
            item_id: itemId,
            size: sizeInfo.size,
            customizations,
        },
        displayName: `${sizeInfo.size.charAt(0).toUpperCase()}${sizeInfo.size.slice(1)} ${item.name}`,
        basePrice: sizeInfo.price,
        customizationItems,
        subtotal,
    };

    const modal = document.getElementById("review-modal");
    const body = document.getElementById("review-body");
    if (!modal || !body) {
        alert("Review modal is unavailable.");
        pendingReview = null;
        return;
    }

    body.innerHTML = renderReviewSummary(pendingReview);
    modal.classList.remove("hidden");
}

async function confirmReviewOrder() {
    if (!pendingReview) {
        return;
    }

    try {
        const res = await fetch(`${API}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(pendingReview.payload),
        });
        if (!res.ok) throw new Error("Order failed");
        closeReviewModal();
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

function renderReceipt(order) {
    if (order.status !== "completed" || !order.receipt) {
        return "";
    }

    const receipt = order.receipt;
    const customizationLines = (receipt.customization_items || [])
        .map(
            (item) =>
                `<li><span>${escapeHtml(item.label)}</span><span>$${Number(item.price).toFixed(2)}</span></li>`
        )
        .join("");

    return `
        <div class="receipt-block">
            <p class="receipt-title">Receipt</p>
            <ul class="receipt-lines">
                <li><span>${escapeHtml(receipt.base_item.label)}</span><span>$${Number(receipt.base_item.price).toFixed(2)}</span></li>
                ${customizationLines}
            </ul>
            <div class="receipt-totals">
                <div><span>Subtotal</span><span>$${Number(receipt.subtotal).toFixed(2)}</span></div>
                <div><span>Tax</span><span>$${Number(receipt.tax_amount).toFixed(2)}</span></div>
                <div class="receipt-grand-total"><span>Total</span><span>$${Number(receipt.total_with_tax).toFixed(2)}</span></div>
            </div>
        </div>
    `;
}

function renderOrder(order) {
    const div = document.createElement("div");
    div.className = "order-item";
    const customizationSummary = formatCustomizationSummary(order.customizations);
    const cancelBtn =
        order.status === "pending"
            ? `<button class="cancel-btn" onclick="cancelOrder(${order.order_id})">Cancel</button>`
            : "";
    const receiptBlock = renderReceipt(order);
    div.innerHTML = `
        <div class="order-info">
            <span class="order-id">#${order.order_id}</span>
            <span class="order-items">${order.items.join(", ")}</span>
            ${customizationSummary}
            <span class="order-price">$${order.total_price.toFixed(2)}</span>
            ${receiptBlock}
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
    document.getElementById("review-back-btn")?.addEventListener("click", closeReviewModal);
    document
        .getElementById("review-confirm-btn")
        ?.addEventListener("click", confirmReviewOrder);

    loadMenu();
    loadOrders();
});
