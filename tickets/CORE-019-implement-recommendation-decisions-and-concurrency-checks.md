# CORE-019 — Implement recommendation decisions and concurrency checks

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-004](CORE-004-add-demo-identity-and-organization-access-checks.md), [CORE-005](CORE-005-implement-append-only-audit-recording.md), [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md), [CORE-015](CORE-015-implement-policy-preview-and-immutable-versions.md)

## Outcome

Record a human decision without changing cash balances or executing a transfer.

## Work to do

- Implement approve/reject/defer/override transitions using the policy and role rules from CORE-001.
- Require reasons for changed amounts; verify current snapshot/policy/source eligibility at decision time.
- Use transactional state changes and a retry/idempotency contract to prevent conflicting decisions.

## Acceptance criteria

- [ ] Superseded or newly blocked recommendations cannot bypass the specified approval eligibility rules.
- [ ] An amount above recommendation requires the elevated role and any policy limits defined in CORE-001.
- [ ] Concurrent or repeated submissions produce one consistent decision and audit outcome.
- [ ] Tests prove decisions never change operating/reserve balances and no transfer path is invoked.

## Out of scope

No bank transfer simulation or external approval messaging.

## Source requirements

MVP: FR-6, DLR-007. See the [source map and shared completion rules](README.md).
