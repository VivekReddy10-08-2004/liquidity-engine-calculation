# CORE-020 — Build human decision controls

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-012](CORE-012-build-the-dashboard-and-calculation-explanation.md), [CORE-019](CORE-019-implement-recommendation-decisions-and-concurrency-checks.md)

## Outcome

Let an authorized user approve, reject, defer, or override the current recommendation.

## Work to do

- Add decision controls, amount editing, required override reason, role/threshold messaging, and saved status.
- Explain that approval records a decision and does not move funds.
- Refresh eligibility before submission and surface conflicts when another change supersedes the recommendation.

## Acceptance criteria

- [ ] A permitted $800K override of the fresh $920K fixture records its reason and saved amount.
- [ ] Blocked/superseded results expose no misleading approve action; server rejection is handled if the UI becomes stale.
- [ ] Double submission cannot create contradictory visible outcomes.
- [ ] UI checks cover viewer permissions, missing reason, conflict, and successful decisions.

## Out of scope

No decision authority for the assistant.

## Source requirements

MVP: FR-6 and Demo Scenario. See the [source map and shared completion rules](README.md).
