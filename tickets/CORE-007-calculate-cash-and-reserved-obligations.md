# CORE-007 — Calculate cash and reserved obligations

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-002](CORE-002-define-domain-and-api-contracts.md)

## Outcome

Compute usable cash and required reserves with an inspectable line-by-line trace.

## Work to do

- Build a pure Decimal-based calculation module with explicit inputs and as-of date.
- Implement restricted-cash exclusion, pending-debit adjustment, horizon/AP filtering, payroll-cycle coverage, and duplicate-payment protection.
- Implement fixed, percentage, and maximum buffer modes plus floor calculation; return included/excluded items and reasons.

## Acceptance criteria

- [ ] The canonical fixture produces $1M required liquidity from its component amounts.
- [ ] Tests cover paid/canceled items, horizon boundaries, overlapping payroll coverage, and a debit linked to an AP obligation.
- [ ] Buffer-mode and rounding examples match CORE-001 exactly.
- [ ] Identical inputs produce identical numeric outputs; the module performs no database, clock, or network reads.

## Out of scope

Action selection and freshness adjustments belong to CORE-008.

## Source requirements

MVP: Core Decision Rules, FR-4, DLR-002. See the [source map and shared completion rules](README.md).
