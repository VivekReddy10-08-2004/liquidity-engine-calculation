# CORE-009 — Persist recommendations and immutable snapshots

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-003](CORE-003-create-database-schema-and-migrations.md), [CORE-005](CORE-005-implement-append-only-audit-recording.md), [CORE-008](CORE-008-apply-freshness-rules-and-choose-recommendations.md)

## Outcome

Generate recommendations that can be reproduced and safely superseded.

## Work to do

- Build the recommendation service to capture financial inputs, source health, policy version, rules version, and calculation time atomically.
- Persist trace and result; define generation/reuse behavior and supersede eligible older recommendations when authoritative inputs change.
- Implement explicit recalculation plus GET dashboard, recommendation detail, and explanation endpoints.

## Acceptance criteria

- [ ] Changing live data or policy does not change a historical explanation.
- [ ] Replaying a stored snapshot under its recorded rules reproduces the result.
- [ ] Dashboard GET requests do not silently create a new recommendation on every refresh.
- [ ] Concurrent generation cannot leave contradictory current recommendations; snapshot/result/audit failures roll back together.

## Out of scope

No UI or decision recording.

## Source requirements

MVP: FR-1, FR-4, recommendations model; architecture: User Journey. See the [source map and shared completion rules](README.md).
