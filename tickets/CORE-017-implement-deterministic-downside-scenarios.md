# CORE-017 — Implement deterministic downside scenarios

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md), [CORE-013](CORE-013-implement-the-daily-liquidity-projection.md)

## Outcome

Compare stress cases using copies of a selected recommendation snapshot.

## Work to do

- Implement POST /api/v1/scenarios for base, revenue delay of 15/30 days, variable AP/card spend +20%, and next payroll +10%.
- Persist scenario assumptions/results with source snapshot reference and audit event; use the same engine and projection rules.
- Return action, allocation delta, warnings, projected low point, and lowest allocation across comparable runs.

## Acceptance criteria

- [ ] Running scenarios leaves source financial records and the base recommendation unchanged.
- [ ] Each transformation affects only the documented items and dates.
- [ ] Revenue-delay allocation and timeline behavior matches CORE-001, including a zero allocation delta if that is the chosen rule.
- [ ] Repeated runs with identical inputs reconcile exactly, and blocked scenarios are not mislabeled as allocatable amounts.

## Out of scope

No probabilistic forecasting or automatic selection of a new policy.

## Source requirements

MVP: FR-5, DLR-006. See the [source map and shared completion rules](README.md).
