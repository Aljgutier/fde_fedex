# 3 - LabNotes AIC-2101

Complete two propose-apply-archive cycles with different levels of review depth

Two features in this lab

propose-apply-archive /...

Two Features
* Drink Customization
* Order confirmation


The dependency: the receipt must show customization details and prices from the first feature. This is the first time a change you build depends on a change you just finished.

You will also learn ... adjusting your review depth, debugging spec-ambiguity


run the system with uv
```
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

# 3.4 Two Drink Customizations

propse-apply-archive ... at a faster pace

prompt 

```
/opsx-propose add-drink-customizations
Customers should be able to add optional extras when ordering any drink:
- Extra espresso shot: +$0.75
- Milk alternative (oat, almond, or soy): +$0.60
- Whipped cream: +$0.50

Customization options should appear on each menu card. The order total
should update dynamically as customizations are selected. The order queue
and status board should display any customizations on each order.

Out of scope: per-drink customization restrictions (all options available
for all drinks), customization inventory tracking, recurring/saved
customization preferences.
```

Verify in the Browser ... http://localhost:8000 ... hard refresh CRL-Shift-R
* customization options visible
* dynamic price updates
* order placement with customizations
* customizations on the status board

Archive the spec ... this automatically archives the currently active spec
```
/opsx-archive
```

ls openspec/specs

# Order Confirmation (2nd feature)
* Reference existing specs ... propose

```
/opsx-propse order-confirmation-receipt
Read the specs in openspec/specs/ for context on the current system,
especially the customization pricing model.

This change adds two things:
1. An order confirmation step: after selecting a drink and customizations,
   the customer sees a "Review Your Order" summary before confirming.
   The summary shows the drink name and size, each selected customization
   with its price, and the order total. The customer can confirm or go back.
2. A receipt view for completed orders: when an order reaches "completed"
   status, it has a receipt showing a line-item breakdown:
   - Base price (drink name, size, price)
   - Each customization as a separate line item with its price
   - Subtotal
   - Total including tax

Out of scope: printing receipts, emailing receipts, receipt history page,
tax configuration UI.
```

Then invoke the proose command ...  with the change name add-order-confirmation-receipt ... AGENT mode

# Fix missing Tax Rate Requirement

Clear context ... fix the spec ... invoke the /apply command 

Open the the spec and add the missing requirement
```
### Requirement: Tax calculation
Tax MUST be calculated at a rate of 8.5%, applied to the order
subtotal (base price plus all customizations). The tax amount
MUST be rounded to the nearest cent using standard rounding
(half-up). Tax MUST appear as a separate line item on the receipt.
```
