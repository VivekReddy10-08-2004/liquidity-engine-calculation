# CORE-021 — Build the audit history API and screen

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-005](CORE-005-implement-append-only-audit-recording.md), [CORE-011](CORE-011-build-the-react-application-foundation.md), [CORE-019](CORE-019-implement-recommendation-decisions-and-concurrency-checks.md)

## Outcome

Allow reviewers to trace an input change through recommendation and decision history.

## Work to do

- Expose a paginated organization-scoped audit API with entity/event/date filters and stable ordering.
- Build an audit timeline showing actor, time, before/after values, reason, and linked recommendation/policy/snapshot.
- Provide recommendation-specific history and clear system-versus-user attribution.

## Acceptance criteria

- [ ] The invoice, recalculation, policy change, scenario, and decision can be traced through linked records.
- [ ] Pagination returns stable, nonduplicated results for an unchanged dataset.
- [ ] Another organization’s history is inaccessible, including through filter manipulation.
- [ ] The screen has useful empty/error states and offers no edit/delete controls.

## Out of scope

No audit export, retention administration, or external log platform.

## Source requirements

MVP: FR-7. See the [source map and shared completion rules](README.md).
