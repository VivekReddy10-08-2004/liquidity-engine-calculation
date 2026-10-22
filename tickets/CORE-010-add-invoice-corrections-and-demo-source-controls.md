# CORE-010 — Add invoice corrections and demo source controls

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-006](CORE-006-build-repeatable-synthetic-data-imports.md), [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md)

## Outcome

Support the demo’s invoice and stale-data changes through audited API operations.

## Work to do

- Add organization-scoped invoice creation and correction/exclusion endpoints with reasons and source provenance.
- Add development-only controls for cash balance and source-health changes so all recommendation states can be demonstrated.
- Trigger recalculation after authoritative changes and return the new recommendation reference.

## Acceptance criteria

- [ ] Adding the $180K in-window invoice changes $1.1M allocation to $920K under the documented fixture policy.
- [ ] Marking payroll stale blocks Allocate, and restoring valid freshness permits a new calculation.
- [ ] Corrections preserve prior snapshots, identify the actor, and create before/after audit events.
- [ ] Invalid edits, duplicate retries, and unauthorized exclusions do not corrupt base records.

## Out of scope

No document extraction or real-source refresh integration.

## Source requirements

MVP: FR-6, Acceptance Criteria, Demo Scenario. See the [source map and shared completion rules](README.md).
