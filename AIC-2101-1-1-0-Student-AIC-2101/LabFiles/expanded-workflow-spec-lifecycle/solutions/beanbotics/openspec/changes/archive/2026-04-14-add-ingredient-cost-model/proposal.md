## Why

BeanBotics currently operates with static pricing for drinks and customizations, but lacks visibility into the actual costs of producing orders. This change introduces an ingredient cost model to calculate the Cost of Goods Sold (COGS) for each order, enabling better financial tracking and margin analysis. By mapping drinks to their ingredient recipes and tracking costs, the business can understand profitability at both the order and aggregate levels through a new financial dashboard.

## What Changes

- Add ingredient definitions with unit costs (espresso shots, milk, chocolate, whipped cream, alternative milks)
- Create drink recipes mapping each drink/size combination to required ingredient quantities
- Implement COGS calculation for orders based on ingredient costs plus customization ingredient costs
- Add financial dashboard displaying total revenue, total COGS, and gross margin
- Include per-order financial breakdown showing revenue, COGS, and margin
- Update order model to include COGS data alongside existing pricing
- Ensure customization surcharges contribute both customer price markup and ingredient cost to COGS

## Capabilities

### New Capabilities
- `ingredient-cost-model`: Define base ingredients with unit costs and manage ingredient data
- `drink-recipe-mapping`: Map each drink/size combination to ingredient quantities required
- `cogs-calculation`: Calculate Cost of Goods Sold for orders based on recipes and customizations
- `financial-dashboard`: Display live financial metrics including revenue, COGS, and margins

### Modified Capabilities
<!-- No existing capabilities are modified - customer pricing behavior remains unchanged -->

## Impact

- Backend: New ingredient and recipe data structures, COGS calculation logic in order service, extended order model
- Frontend: New financial dashboard component alongside order board, per-order margin display
- Data: New ingredient cost data file, recipe mappings in menu data
- APIs: Order responses include COGS data, new endpoint for financial summary if needed</content>
<parameter name="filePath">/Users/joemirza/beanbotics/openspec/changes/add-ingredient-cost-model/proposal.md