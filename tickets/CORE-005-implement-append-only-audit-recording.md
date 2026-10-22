# CORE-005 — Implement append-only audit recording

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-004](CORE-004-add-demo-identity-and-organization-access-checks.md)

## Outcome

Record who changed what and preserve the decision context.

## Work to do

- Create an audit service with event types for imports, corrections, recommendations, policies, scenarios, and decisions.
- Capture organization, actor/role, before/after data, reason, timestamp, and applicable snapshot/policy/rules references.
- Provide transaction-aware event insertion for other services and prevent application updates/deletes to historic audit events.

## Acceptance criteria

- [ ] A failed business transaction does not leave a misleading success event.
- [ ] Application update/delete attempts on stored audit records fail.
- [ ] Audit payloads preserve the previous value when the source record changes.
- [ ] Tests verify organization scoping and system-actor attribution.

## Out of scope

Audit browsing UI belongs to CORE-021; no claim of protection against a database administrator.

## Source requirements

MVP: FR-7. See the [source map and shared completion rules](README.md).
