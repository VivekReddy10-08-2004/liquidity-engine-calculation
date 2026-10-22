# CORE-003 — Create database schema and migrations

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-002](CORE-002-define-domain-and-api-contracts.md)

## Outcome

Persist the core records in PostgreSQL with explicit organization boundaries.

## Work to do

- Configure SQLAlchemy sessions, transaction handling, and Alembic using the existing settings.
- Add tables for organizations/users, accounts, obligations, receivables, source health, policy versions, snapshots, recommendations, scenario results, decisions, and audit events.
- Use numeric money columns, organization-aware relationships, uniqueness constraints for imported source versions, and indexes for tenant/date lookups.

## Acceptance criteria

- [ ] Migrations initialize an empty PostgreSQL database and upgrade it to the current revision.
- [ ] Cross-organization references and duplicate source/version keys are rejected by constraints.
- [ ] Database round-trip tests preserve exact amounts and timestamps.
- [ ] Document startup/migration commands and verify against real PostgreSQL; Docker must be available for local container checks.

## Out of scope

No business endpoints or production deployment.

## Source requirements

MVP: Data Model and Technical Approach. See the [source map and shared completion rules](README.md).
