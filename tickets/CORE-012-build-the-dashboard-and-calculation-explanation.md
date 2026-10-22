# CORE-012 — Build the dashboard and calculation explanation

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md), [CORE-010](CORE-010-add-invoice-corrections-and-demo-source-controls.md), [CORE-011](CORE-011-build-the-react-application-foundation.md)

## Outcome

Let a user see the current recommendation and reconcile its amount without AI.

## Work to do

- Render cash/reserve totals, required liquidity, action/amount, horizon, confidence, timestamp, and source health.
- Build the explanation view from the saved trace with included/excluded records, buffer math, policy/rules versions, and snapshot references.
- Add demo-load, add-invoice, correction, and source-health controls backed by CORE-010.

## Acceptance criteria

- [ ] The base screen displays $1.1M allocation and the explanation totals match exactly.
- [ ] Adding an invoice updates the current result while the old explanation remains accessible.
- [ ] Every blocked result identifies the source, last refresh, and practical impact.
- [ ] Loading, empty, API failure, and stale-data states are covered in UI checks; narrow layouts and keyboard navigation remain usable.

## Out of scope

Timeline, policy editor, and decisions have separate tickets.

## Source requirements

MVP: FR-1, FR-4, FR-8. See the [source map and shared completion rules](README.md).
