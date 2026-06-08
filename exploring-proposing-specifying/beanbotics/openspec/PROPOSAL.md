
# Explore Status Lifecycle

Here is what we do in this lab
* Explore ... "ask" analysis
* Agent ... Create draft proposal
* Agent ... propose using the /opsx-propose ... change ... add-order-status-lifecycle
  * propsal.md
  * specs/
  * design.md
  * tasks.md
* Review the artifacts
* /apply command to /opsx-apply ... implement
* Archive change ... /opsx-archive ... marks the feature as complete and saves the artifacts ... design etc 


## Problem

The Order model documents a multi-step lifecycle (`pending`, `preparing`, `ready`, `completed`, `cancelled`), but the implementation only uses `pending` and `cancelled`. This creates a gap between the documented domain model and actual runtime behavior.

Today:
- New orders are always `pending`.
- Orders can be cancelled only while `pending`.
- No mechanism exists to advance orders through `preparing`, `ready`, or `completed`.
- The queue UI cannot represent operational progress beyond pending/cancelled.

As a result, staff cannot track order progress in-system, and customers/admins cannot distinguish in-progress versus fulfilled orders.


Draft proposal
Prompt
```
Good analysis. Let's capture this as a draft proposal summary.
Here are my decisions on the open questions:

- Advance buttons inline on each order in the existing UI (no separate
  staff view, no automatic timers)
- Cancel from pending only (keep the current restriction)
- Completed orders stay visible in a "Completed" group on the queue board
- Single endpoint for all status transitions with a transition map
  that validates and rejects invalid moves

Write a draft proposal summary with these decisions baked in.
Include: the problem, proposed solution, scope, out of scope, and risks.
Save it to docs/explore-status-lifecycle.md.
```


Saved to docs/explore-statis-lifecycle.md


# 2.5 Propse the order Lifecycle

Invoke the propose command

Prompt
```
/opsx-propose

Change name: add-order-status-lifecycle

Read docs/explore-status-lifecycle.md and propose a change that introduces an order status lifecycle.

The change should define clear states (e.g., pending, confirmed, fulfilled, cancelled) and transitions between them.

Ensure the proposal reflects the patterns and requirements described in the document.
```

Quick orientation. Before diving into a detailed review, get a quick sense of what was generated. In your terminal:

ls openspec/changes/add-order-status-lifecycle/
You should see:
* proposal.md
* specs/
* design.md
* tasks.md

In the previous lab, you glanced at these artifacts and moved on. This time, you will read each one carefully and make improvements.


```text
Proposal: proposal.md
Summary: Defines why the lifecycle change is needed, what will change, introduces the new capability order-status-lifecycle, and lists backend/frontend impact.

Design: design.md
Summary: Documents architecture decisions, transition map, single endpoint strategy, inline UI controls, risks, migration plan, and open questions.

Specs: spec.md
Summary: Adds normative requirements and scenarios for lifecycle statuses, transition validation, pending-only cancellation, queue grouping, and inline actions.

Tasks: tasks.md
Summary: Provides dependency-ordered implementation checklist for backend changes, frontend changes, and verification coverage.
```

# 2.6 Review and Refine
prompt
```

/opsx-apply

Change name: add-order-status-lifecycle

Implement the change using proposal.md, design.md, spec.md, and tasks.md.

```