# 4 - Expanded Workflow Lab Notes

 Previous labs
 * you used the core workflow: propose, apply, archive. Each time, the propose command generated all four artifacts (proposal, specs, design, and tasks) in a single step. You reviewed the artifacts after they were all generated and made corrections before applying.

 That works well for features you can describe in one prompt, but some features have too many interrelated decisions.

 This lab 
 * introduces the expanded workflow. Instead of generating all artifacts at once, you build them one at a time with review gates betweenn each step
 * You review the specs before the design is generated. Each correction compounds. Downstream artifacts benefit from the reviewed upstream artifacts.

 Lab Setup
    * uv venv
    * install packages
    * run beanbotics app with uv

Features
* The feature: Ingredient cost model with a financial dashboard. Each drink is a recipe that consumes specific quantities of base ingredients. The financial dashboard shows revenue, cost of goods sold (COGS), and gross margin, updating live as orders are placed and completed.
* Why this feature needs the expanded workflow: The ingredient cost model involves multiple interrelated decisions. Ingredient definitions, recipe mappings per drink and size, COGS calculations that account for customizations, and a live financial view that aggregates across orders. Before you start, consider: could you write a single proposal prompt that captures all of this with enough precision that the AI gets it right on the first pass?



Starting State
* ls openspec/specs
* You should see seven spec files covering four domain areas from the previous labs: drink size selection, order status lifecycle (two specs), drink customizations (two specs), and order confirmation with receipts (two specs).

Commands Github CoPilot
* .github/prompts/

```
----                 -------------         ------ ----                                                                                                      
-a----         5/28/2026   2:49 PM           4515 opsx-apply.prompt.md                                                                                      
-a----         5/28/2026   2:49 PM           4934 opsx-archive.prompt.md                                                                                    
-a----         5/28/2026   2:49 PM           7459 opsx-bulk-archive.prompt.md                                                                               
-a----         5/28/2026   2:49 PM           4876 opsx-continue.prompt.md                                                                                   
-a----         5/28/2026   2:49 PM           6667 opsx-explore.prompt.md                                                                                    
-a----         5/28/2026   2:49 PM           4167 opsx-ff.prompt.md                                                                                         
-a----         5/28/2026   2:49 PM           2585 opsx-new.prompt.md                                                                                        
-a----         5/28/2026   2:49 PM          13995 opsx-onboard.prompt.md                                                                                    
-a----         5/28/2026   2:49 PM           4335 opsx-propose.prompt.md                                                                                    
-a----         5/28/2026   2:49 PM           4280 opsx-sync.prompt.md                                                                                       
-a----         5/28/2026   2:49 PM           6410 opsx-verify.prompt.md     
```


**Switcch to the Expanded Profile**

Add 
* New Change
* Continue change
* Fast Forward
* Verify Change

**Scafold and Build the Proposal**

Invoke the new command
```
/opsx-new  add-ingredient-cost-model
```


Generate the proposal ... prompt

```
/opsx-propose add-ingredient-cost-model  <<< proposal name here is optional
Read the specs in openspec/specs/ for context on the current system.

This change adds an ingredient cost model and financial dashboard.

Ingredient cost model:
- Define base ingredients with unit costs (espresso per shot,
  milk per oz, chocolate per oz, whipped cream per serving,
  alternative milk per oz)
- Map each drink/size to ingredient quantities — e.g., a Large
  Neural Network Latte uses 2 espresso shots + 12oz milk. Small and
  medium drinks typically use 1 shot; large drinks use 2.
- Calculate COGS per order from the recipe ingredients
- Customization surcharges (like extra shot) must also add their
  ingredient cost to COGS, not just the customer price

Financial dashboard:
- Display alongside the order board showing total revenue,
  total COGS, and gross margin (revenue minus COGS)
- Per-order breakdown showing revenue, COGS, and margin per order
- Updates live as orders are placed and completed

Out of scope: supplier management, ingredient inventory tracking,
purchase ordering, historical reporting, multi-location support.

Then run the continue command. Generate the proposal only and stop --
I will review it before continuing.
```

**Verify new commands**
The new commands should be available in your agent immediately. Verify by checking your agent’s command directory (see the table in Exercise 1 step 5). For example, Claude Code users would run:

ls .claude/commands/opsx/


**Pass the Review Gate** ... 
* is the scope right
* are customization costs in scope for COGS
* Is there anything in scope that should not be

```
/opsx-continue
```

**Cloear Context and apply**
```
/opsx-apply
```

**Invoke the verify command to the implementation against the specs**

Agent reads the specs and checks for three things
Completeness: Are all requirements implemented? Are all tasks done?

* Correctness: Does the implementation match the spec’s intent?
* Coherence: Do design decisions show up in the code?
* Review the verify output. It may surface issues you did not catch during manual testing. Particularly requirements that were implemented incorrectly or not at all.


**The customization COGS test**
This is the critical verification. Place a specific test order and check whether the COGS calculation is correct:

* Place an order for a Large Neural Network Latte ($6.50) with an extra espresso shot (+$0.75)
* Advance the order through the lifecycle to completed
* Check the financial dashboard
* Calculate the expected COGS by hand:**


**Fix any issues.** 

If verify or manual testing found problems:

Spec gap (customization COGS missing): If the COGS calculation ignores customization ingredients, the spec may not have required it explicitly. Open the spec file in openspec/changes/add-ingredient-cost-model/specs/ and add or strengthen the requirement:

prompt
```
### Requirement: COGS includes customization ingredient costs
COGS for an order MUST include the ingredient cost of every
customization. An extra espresso shot MUST add the cost of one
espresso shot ($0.40) to the order's COGS. The COGS displayed on
the financial dashboard MUST reflect the full ingredient cost
including customizations.
```

**Archive**
```
/opsx-archive
```