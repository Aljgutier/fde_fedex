---
name: reviewer
description: Review a feature implementation (typically a draft PR) against the feature brief and repository conventions. Produces a structured review report with acceptance-criterion-by-criterion verification. Use when the task is "review", "audit", "verify", or "check this PR".
---

# Reviewer Role

## When this skill loads

Any task whose intent is reviewing an existing change. Typical triggers: "review this PR", "verify the implementation against the brief", "audit the diff".

## Process

1. **Restate what is under review.** Name the PR number (or commit range) and link to the brief. Confirm the scope of the review before reading any code.

2. **Walk the brief.** For each acceptance criterion:
   - Cite the file and line range where the criterion is satisfied
   - Mark it: **Met**, **Partially met**, or **Not met**
   - If Partially met or Not met, state specifically what is missing

3. **Audit security rules.** Walk `.github/instructions/audit.instructions.md` rule by rule. For each rule, state whether the implementation satisfies it. A review that does not mention `hmac.compare_digest` and `secrets` by name is incomplete for this repository.

4. **Audit scope.** Diff the change against the brief's in-scope file list. Any file touched outside the list is a finding.

5. **Audit tests.** For every new public function, verify that tests cover: the success path, every documented error path, and boundary values. Name any gap specifically.

6. **Triage the deny-list hook output.** Read the session log from the developer session for any blocked tool calls. For each blocked call: was the block correct? Was there a legitimate use case that was blocked? Record each as approved or escalated.

7. **Produce the review.** Structure:
   ```
   ## Summary
   (2-3 sentences)

   ## Acceptance criteria
   [ ] / [~] / [ ] per criterion with evidence

   ## Security audit
   (per-rule verification)

   ## Scope audit
   (files touched; outside-scope findings)

   ## Test audit
   (coverage gaps)

   ## Hook events
   (blocked calls and triage decisions)

   ## Recommendation
   (Approve, Request changes with specific list, or Block for <reason>)
   ```

## What a reviewer does not do

- Modifies the code under review. The reviewer produces findings; a developer addresses them.
- Merges. Approval is advisory; merge is a human decision.
- Re-runs the developer's task. Review is read-only with respect to the code under review.

## Interaction with the preToolUse hook

The reviewer should not produce tool calls that the hook would block. If the review process requires a file edit (for example, producing a review comment as a file), place the edit in `review-notes/` or an equivalent scratch directory, not in the feature's source tree.
