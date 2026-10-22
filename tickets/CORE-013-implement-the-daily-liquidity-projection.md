# CORE-013 — Implement the daily liquidity projection

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-007](CORE-007-calculate-cash-and-reserved-obligations.md), [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md)

## Outcome

Provide dated cash projections for the timeline and scenarios.

## Work to do

- Create a deterministic daily projection service and GET /api/v1/recommendations/{id}/timeline.
- Use snapshot data to list inflows/outflows, opening/closing balances, item states, and daily low point for a 30-day view.
- Explain how the view relates to a 7–60-day policy horizon and whether it represents pre-allocation or hypothetical post-allocation balances under CORE-001.

## Acceptance criteria

- [ ] Each day reconciles opening balance plus eligible receipts minus eligible outflows to closing balance.
- [ ] Paid records and pending debits already reflected in cash are not subtracted twice.
- [ ] Expected receipts remain distinguishable from cleared cash; no timeline forecast overwrites recommendation facts.
- [ ] Tests cover same-day events, empty days, overdue items, and policy/view horizon differences.

## Out of scope

No statistical forecasting or UI chart.

## Source requirements

MVP: FR-2 and FR-5. See the [source map and shared completion rules](README.md).
