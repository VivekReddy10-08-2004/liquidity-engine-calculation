# CORE-014 — Build the liquidity timeline view

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-011](CORE-011-build-the-react-application-foundation.md), [CORE-013](CORE-013-implement-the-daily-liquidity-projection.md)

## Outcome

Show when obligations fall due and where projected cash is lowest.

## Work to do

- Render a 30-day balance chart and dated event list from the timeline endpoint.
- Distinguish confirmed, expected/uncertain, pending, and completed items using labels as well as color.
- Show receipt assumptions, policy horizon, low point, and projection basis.

## Acceptance criteria

- [ ] Selecting a date reveals matching source events and amounts.
- [ ] Chart balances agree with the API; a readable table/list provides the same information.
- [ ] Long labels, no-event days, loading, and error states remain usable.
- [ ] UI tests verify state labels and exact displayed values from a known fixture.

## Out of scope

No separate browser calculation engine.

## Source requirements

MVP: FR-2. See the [source map and shared completion rules](README.md).
