# Lab Notes AIC-2101 foundations

Propose-Apply-Archive cycle

* openspec command /opsx-propose
* verify openspec is installed ... openspec --version
* see the openspec files in ./openspec
* config.yaml ...  replace config.yaml (section 1.5)... configure the project context ... replace contents of config.yaml with the following

```sh
schema: spec-driven

context: |
  BeanBotics is an AI-themed coffee ordering web application.
  Tech stack: Python 3.10+, FastAPI, vanilla HTML/CSS/JavaScript frontend.
  Backend: FastAPI app in backend/ with service layer pattern.
  Frontend: Single-page app in frontend/ using fetch API for all server calls.
  Data: Menu items loaded from backend/data/menu.json. Orders stored in memory.
  No database, no authentication, no payment processing.
  API endpoints: GET /api/menu, POST /api/orders, GET /api/orders, DELETE /api/orders/{id}.
```
* Agents.md
     AGENTS.md: already in the project. You (the developer) write and maintain this. It tells your agent about the project: tech stack, structure, conventions. AGENTS.md is an emerging cross-agent convention that most listed agents read directly; a few (like Claude Code) also read a tool-specific file such as CLAUDE.md, but AGENTS.md is the agent-neutral source of truth in this course.


* explore the code base iwth your agent (section 1.6)
* **propose-apply-archive** cycle 



* Clear your context

the above will create artifacts ... propose.md, ./spec ... tasks.md

* Ask the agent
```text
What would need to change to let customers choose between small, medium, and large sizes when ordering?
```

* propse the feature
```text
/opsx-propose
Add a size selector (small, medium, large) to the order form so
customers can choose a size before placing an order. The selected
size should drive the displayed price and be sent with the order.

Out of scope: drink customizations (milk, flavor, extra shots),
menu changes, new backend endpoints, and any UI changes beyond
the size selector and its price display.
The first argument add-drink-size-selection is 
```

* apply the change  ... tells the agent to apply the change ... watch as the agent goes through tasks in tasks.md
```
/opsx-apply
```

* verify the feature ... manually explore the UI

* Archive the change

```text
/opsx-archive
```