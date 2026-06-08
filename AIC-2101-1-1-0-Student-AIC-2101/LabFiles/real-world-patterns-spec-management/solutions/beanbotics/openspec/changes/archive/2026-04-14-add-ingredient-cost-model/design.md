## Context

BeanBotics currently uses static pricing for menu items and customizations loaded from `menu.json`, with no tracking of production costs. Orders are stored in memory with basic pricing information. The system supports drink sizes, customizations, and order status lifecycle, but lacks financial cost analysis capabilities. This change adds ingredient-based cost calculation to enable COGS tracking and margin analysis through a financial dashboard.

## Goals / Non-Goals

**Goals:**
- Implement ingredient cost model with base ingredient unit costs
- Map drink recipes to ingredient quantities for COGS calculation
- Calculate per-order COGS including customization ingredient costs
- Display financial dashboard with revenue, COGS, and margin metrics
- Maintain backward compatibility with existing pricing and API contracts
- Enable real-time financial tracking as orders are placed and completed

**Non-Goals:**
- Supplier management or purchase ordering systems
- Ingredient inventory tracking or stock management
- Historical financial reporting or data persistence
- Multi-location support or advanced analytics
- Changes to customer-facing pricing logic

## Decisions

**Ingredient Data Storage**: Create a new `ingredients.json` file defining base ingredients with unit costs (espresso per shot: $0.40, milk per oz: $0.08, etc.). This separates cost data from menu pricing for maintainability.

**Recipe Mapping**: Extend `menu.json` with a `recipe` field per size containing ingredient quantities (e.g., "large": {"espresso": 2, "milk": 12}). This keeps recipes co-located with menu items while allowing size-specific variations.

**COGS Calculation**: Add COGS calculation to `OrderService.create_order()` method. Calculate base drink cost from recipe × ingredient costs, plus customization ingredient costs. Store COGS in Order model alongside existing pricing fields.

**Customization Cost Mapping**: Define ingredient costs for customizations in `ingredients.json` (e.g., "extra-shot": {"espresso": 1}, "oat-milk": {"oat-milk": 8}). This ensures customizations contribute both customer surcharge and ingredient cost to COGS.

**Financial Dashboard**: Create new frontend component that aggregates order data to show total revenue, COGS, and gross margin. Update live as orders change status. Position alongside existing order board for operational visibility.

**Order Model Extension**: Add `cogs` field to Order dataclass to store calculated cost. Include in API responses for frontend consumption without breaking existing contracts.

## Risks / Trade-offs

**Data Maintenance Complexity**: Adding ingredient costs and recipes increases data maintenance burden. Manual updates required when costs change. → Mitigation: Clear documentation and validation in data loading.

**Calculation Performance**: COGS calculation on every order could impact performance if recipes become complex. → Mitigation: Pre-calculate and cache ingredient costs, keep recipes simple.

**Cost Data Accuracy**: Inaccurate ingredient costs or recipes could lead to incorrect financial reporting. → Mitigation: Input validation and clear separation of cost vs. selling price data.

**Frontend Complexity**: Adding financial dashboard increases frontend complexity and potential for display bugs. → Mitigation: Isolate dashboard component, thorough testing of calculations.</content>
<parameter name="filePath">/Users/joemirza/beanbotics/openspec/changes/add-ingredient-cost-model/design.md