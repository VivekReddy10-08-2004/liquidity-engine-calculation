# CORE-023 — Package the local demo and project handoff

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-022](CORE-022-verify-the-complete-mvp-and-automate-ci.md)

## Outcome

Let a reviewer start the complete MVP and understand it quickly.

## Work to do

- Add backend/frontend Dockerfiles and extend compose.yaml to run the full app with health checks and migration/seed instructions.
- Write setup, API, data dictionary, architecture, limitations, and a 90-second demo script; include screenshots.
- Document safe demo reinitialization and preserve the explicit synthetic-data/no-execution boundary.

## Acceptance criteria

- [ ] One documented command starts a clean local stack and allows demo data loading.
- [ ] A new reviewer can reproduce the $1.1M to $920K invoice change, inspect the trace, and record an eligible decision.
- [ ] The script restores freshness and regenerates before approval if it previously demonstrated a stale-data block.
- [ ] Document verified commands and remaining limitations; do not describe the MVP as production-ready.

## Out of scope

Public hosting is a separate optional ticket; no live financial integrations.

## Source requirements

MVP: DLR-008, Demo Scenario, Definition of Done. See the [source map and shared completion rules](README.md).
