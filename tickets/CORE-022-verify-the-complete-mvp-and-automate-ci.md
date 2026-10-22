# CORE-022 — Verify the complete MVP and automate CI

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-012](CORE-012-build-the-dashboard-and-calculation-explanation.md), [CORE-014](CORE-014-build-the-liquidity-timeline-view.md), [CORE-016](CORE-016-build-the-policy-editor-and-version-comparison.md), [CORE-018](CORE-018-build-scenario-comparison-controls.md), [CORE-020](CORE-020-build-human-decision-controls.md), [CORE-021](CORE-021-build-the-audit-history-api-and-screen.md)

## Outcome

Make the finished workflow repeatable and catch regressions automatically.

## Work to do

- Add Playwright coverage for demo import, explanation, invoice change, scenario, stale payroll, restored freshness, override, and audit verification.
- Run lint, formatting, typing, frontend build, domain/API/PostgreSQL tests, and end-to-end checks in GitHub Actions.
- Add financial invariant/property checks where valuable and enforce at least 90% branch coverage specifically on the core liquidity engine.

## Acceptance criteria

- [ ] All four recommendation states are demonstrated by deterministic fixtures.
- [ ] The complete workflow passes from a clean database with a controlled clock.
- [ ] CI fails for a financial reconciliation error, authorization regression, or failed workflow.
- [ ] Coverage does not hide engine gaps behind bootstrap files; meaningful tests remain owned by their feature tickets.

## Out of scope

AI evaluations belong to AI-005; this ticket does not defer all testing until the end.

## Source requirements

MVP: Acceptance Criteria, DLR-008, Definition of Done. See the [source map and shared completion rules](README.md).
