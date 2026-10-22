# AI-006 — Generate a daily treasury brief

**Status:** Backlog  
**Release:** Future AI enhancement  
**Depends on:** [AI-005](AI-005-build-the-assistant-panel-and-evaluation-gate.md)

## Outcome

Summarize already-calculated facts in a concise read-only brief.

## Work to do

- Implement an on-demand daily-brief endpoint and UI using the authorized evidence pack and validated output pipeline.
- Include the selected recommendation, key drivers, freshness warnings, and available scenario reference.
- Record source context, generated time, model/prompt version, and query outcome.

## Acceptance criteria

- [ ] Every financial claim matches deterministic evidence; absent scenario results are not invented.
- [ ] A brief identifies the as-of snapshot and does not imply continuous freshness.
- [ ] No brief changes a recommendation or sends an external message.
- [ ] Tests cover missing evidence, stale payroll, provider failure, and unsupported numeric output.

## Out of scope

No scheduled email/Slack delivery or autonomous recommendations.

## Source requirements

RAG: Phase 2A and DLR-008. See the [source map and shared completion rules](README.md).
