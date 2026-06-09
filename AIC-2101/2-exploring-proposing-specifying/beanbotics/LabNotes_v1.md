# Lab Notes BeanBotics

propose - apply - archive 

* explore ... ask prompt
* **propose** ...fresh context... /ospx-propse + prompt ...  name the feature
* review the plan  ... manually
* **apply**  ... /ospx-apply
* verify ... verify the implementation
* **archive** ... /ospx-archive

**Explore (Section2.4)** ... ask free form explore ... not /opsx command
  * ask agent ... expore Ask prompt  ... if we wanted to active full order cycle

  ```
  If we wanted to activate the full order lifecycle -- pending through
    preparing, ready, and completed -- what would need to change? Think
    about both the backend (API, validation) and the frontend (how would
    the order queue display different statuses?).
  ```
  * confirm the analysis

**Draft proposal Prompt (Section 2.5)** ... /opsx-proose
* erase context  
* /opsx-propose ... notice save to below ... PROMPT
```text
/opsx-propose add-order-status-lifecycle
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
* Documents created
  * proposal.md
  * specs/
  * design.md
  * tasks.md

**Manually review and Refine (use AI)**

** clear context 
* ./openspeck/changes/add-order-status-lifecycle/propoasl.md
    *  are scenarios concrete
    * is there scenario for invalid transactions
    * review the design ... 

**Apply ... verify ... archive ... the Refined Specs** (Section 2.7)

* invoke the apply command ... /opsx-apply
* verify the ... manually
* arvhive the feature ... /opsx-archive
