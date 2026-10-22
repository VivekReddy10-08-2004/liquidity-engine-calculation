# CORE-015 — Implement policy preview and immutable versions

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-005](CORE-005-implement-append-only-audit-recording.md), [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md)

## Outcome

Allow governed policy changes while preserving the policy behind every past result.

## Work to do

- Add list/detail, preview, and create-version endpoints for all documented policy fields.
- Enforce allowed horizons, payroll cycles, AP windows, buffer modes, destination labels, approval thresholds, and effective-time rules.
- Preview against a fixed snapshot; activation generates a new recommendation and records policy audit events.

## Acceptance criteria

- [ ] Saving a policy creates a new version; existing policy records cannot be edited in place.
- [ ] Preview makes no authoritative changes and returns its policy/snapshot context.
- [ ] Historic recommendations retain their original policy; concurrent saves cannot silently overwrite the active version.
- [ ] Role checks and tests cover invalid values, effective dates, and policy-driven recalculation.

## Out of scope

No natural-language policy drafting.

## Source requirements

MVP: FR-3, DLR-005. See the [source map and shared completion rules](README.md).
