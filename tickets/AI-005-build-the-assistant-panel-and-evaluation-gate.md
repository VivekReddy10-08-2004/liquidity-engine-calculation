# AI-005 — Build the assistant panel and evaluation gate

**Status:** Backlog  
**Release:** Optional RAG release  
**Depends on:** [AI-004](AI-004-build-cited-assistant-answers-and-query-audit.md), [CORE-012](CORE-012-build-the-dashboard-and-calculation-explanation.md)

## Outcome

Expose understandable cited answers and verify the optional assistant before release.

## Work to do

- Add recommendation-scoped chat with clickable evidence references, answer status, and unavailable/refusal states.
- Create a curated evaluation dataset for numeric consistency, citations, stale/missing evidence, history, tenant isolation, and prompt injection.
- Run deterministic adapter/validator evaluations in CI; document opt-in live-model evaluations and explicit release thresholds.

## Acceptance criteria

- [ ] Users can navigate from a factual answer to its authorized supporting record.
- [ ] All required security and grounding cases pass the recorded release thresholds.
- [ ] Switching recommendations cannot leak the previous conversation’s evidence.
- [ ] The AI demo explains the invoice change and refuses approval/transfer; the normal explanation remains fully usable with AI disabled.

## Out of scope

No claim that citations alone prove correctness; no dependency for core MVP release.

## Source requirements

RAG: Evaluation suite, DLR-007, DLR-009, RAG demonstration. See the [source map and shared completion rules](README.md).
