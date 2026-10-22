# CORE-002 — Define domain and API contracts

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-001](CORE-001-resolve-calculation-and-workflow-rules.md)

## Outcome

Represent cash, obligations, policies, and decisions consistently across imports, storage, and API responses.

## Work to do

- Create Pydantic contracts and enums for accounts, obligations, receivables, source health, policies, snapshots, recommendations, decisions, and audit events.
- Specify UUID identifiers, organization ownership, UTC timestamps, business-date semantics, decimal-string money, currency and amount validation.
- Document endpoint payloads and structured errors in docs/api-contract.md; include imports, invoice creation/correction, source-health controls, policy preview, timeline, and recalculation.

## Acceptance criteria

- [ ] Contract tests reject malformed dates, unsupported currency, invalid policy options, and invalid amounts according to CORE-001.
- [ ] Money round-trips without floating-point loss; example IDs match the declared identifier type.
- [ ] Contracts include source identifiers, versions, pending-debit linkage, and all fields needed to explain inclusion/exclusion.
- [ ] Documented request/response examples validate against the schemas.

## Out of scope

No engine or database implementation.

## Source requirements

MVP: Data Model, API Contract, DLR-001. See the [source map and shared completion rules](README.md).
