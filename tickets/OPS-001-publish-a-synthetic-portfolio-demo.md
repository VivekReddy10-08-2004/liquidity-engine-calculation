# OPS-001 — Publish a synthetic portfolio demo

**Status:** Backlog  
**Release:** Optional hosting  
**Depends on:** [CORE-023](CORE-023-package-the-local-demo-and-project-handoff.md)

## Outcome

Make the completed demo available through a shareable URL when a hosting target is selected.

## Work to do

- Choose a hosting provider and document required services, configuration, demo identity, and deployment steps.
- Configure HTTPS, API/frontend connectivity, migration rollout, and isolated/resettable synthetic demo state.
- Keep provider secrets in deployment configuration and write an update/rollback procedure.

## Acceptance criteria

- [ ] The deployed app completes the documented demo flow and clearly identifies synthetic data.
- [ ] One visitor cannot corrupt another visitor’s demo state; define isolation/reset behavior.
- [ ] Health checks and basic failure logs work, and repository/configuration contain no real credentials.
- [ ] Record the verified URL and deployment revision after deployment actually succeeds.

## Out of scope

Optional portfolio delivery; no production customer accounts or real finance data.

## Source requirements

MVP: Technical Approach deployment options; RAG: DLR-009. See the [source map and shared completion rules](README.md).
