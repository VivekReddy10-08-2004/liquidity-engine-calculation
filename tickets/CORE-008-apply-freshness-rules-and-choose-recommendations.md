# CORE-008 — Apply freshness rules and choose recommendations

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-007](CORE-007-calculate-cash-and-reserved-obligations.md)

## Outcome

Convert calculated liquidity and source health into one safe, explainable result.

## Work to do

- Implement fresh/warning/stale/error classification using explicit evaluation time and the thresholds from CORE-001.
- Retain known stale AP obligations, apply defined conservative adjustments, and calculate deterministic confidence.
- Select Allocate, Hold, Pull Back, or Review Required with amount, blocking reasons, and remaining shortfall.

## Acceptance criteria

- [ ] Stale/missing bank or payroll data never produces Allocate.
- [ ] A reserve pull-back is capped at usable reserve cash and exposes any uncovered shortfall.
- [ ] Known stale AP remains reserved; warning impact reconciles to the trace.
- [ ] Tests cover exact freshness boundaries, equality, conflicts, uncategorized critical obligations, and every action branch.

## Out of scope

No autonomous refresh jobs or money movement.

## Source requirements

MVP: Fail-safe requirements, FR-8, DLR-003. See the [source map and shared completion rules](README.md).
