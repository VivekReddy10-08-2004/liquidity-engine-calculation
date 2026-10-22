# CORE-004 — Add demo identity and organization access checks

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-003](CORE-003-create-database-schema-and-migrations.md)

## Outcome

Ensure every request operates as a known demo user within one organization.

## Work to do

- Add a development identity adapter and server-side organization/role resolution.
- Apply ownership checks to repositories and endpoint dependencies, including recommendation history and imports.
- Define viewer, controller, and elevated demo-role capabilities using CORE-001; document the development-only identity mechanism.

## Acceptance criteria

- [ ] Two-organization tests prove users cannot read or mutate each other’s records by changing a URL or payload.
- [ ] Actor ID and role come from resolved identity, not a trusted request-body assertion.
- [ ] Unauthorized actions produce consistent errors without exposing another organization’s record contents.
- [ ] Demo identity cannot silently act as production authentication.

## Out of scope

No external identity-provider integration or customer onboarding.

## Source requirements

MVP: Target Users, Auth, tenant-scoped contracts; RAG: Access control. See the [source map and shared completion rules](README.md).
