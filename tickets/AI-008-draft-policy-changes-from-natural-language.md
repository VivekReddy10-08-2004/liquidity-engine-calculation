# AI-008 — Draft policy changes from natural language

**Status:** Backlog  
**Release:** Future AI enhancement  
**Depends on:** [AI-005](AI-005-build-the-assistant-panel-and-evaluation-gate.md), [CORE-016](CORE-016-build-the-policy-editor-and-version-comparison.md)

## Outcome

Offer an optional policy draft that users inspect through the existing editor.

## Work to do

- Translate a request into allowlisted policy fields with typed validation and a field-level diff.
- Explain ambiguous/unsupported requests without silently inventing policy settings.
- Pass the draft to the normal preview/editor workflow; only its explicit human save creates a version.

## Acceptance criteria

- [ ] An assistant request by itself never saves or activates a policy.
- [ ] Out-of-range values and unsupported policy features are rejected.
- [ ] The saved version, if confirmed, retains human actor and draft provenance.
- [ ] Tests cover ambiguity, injection, validation errors, cancellation, and explicit confirmation through the existing workflow.

## Out of scope

Future enhancement; no model-owned policy activation or financial recommendation.

## Source requirements

RAG: Phase 3 — Policy draft assistant. See the [source map and shared completion rules](README.md).
