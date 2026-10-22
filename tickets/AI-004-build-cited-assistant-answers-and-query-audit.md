# AI-004 — Build cited assistant answers and query audit

**Status:** Backlog  
**Release:** Optional RAG release  
**Depends on:** [AI-003](AI-003-retrieve-authorized-evidence-for-a-recommendation.md)

## Outcome

Answer recommendation questions using validated evidence while refusing financial actions.

## Work to do

- Implement POST /api/v1/recommendations/{id}/assistant with fixed grounded/insufficient_evidence/refused_out_of_scope/error statuses.
- Validate citations and factual amount/date/status claims against the evidence pack before returning a response.
- Record actor, retrieved sources, prompt/model versions, response hash/status, latency, and usage in append-only query events.

## Acceptance criteria

- [ ] The invoice-change answer cites both comparable results and the supporting obligation/policy evidence.
- [ ] Unsupported numbers, missing citations, and contradictory action claims are rejected or replaced by a controlled fallback.
- [ ] Approval, transfer, policy mutation, investment advice, and cross-tenant prompts cannot cause actions.
- [ ] Provider failure still leaves an appropriate query outcome; core financial records are unchanged.

## Out of scope

No invoice extraction, daily brief, or assistant write authority.

## Source requirements

RAG: Response Contract, AI Security, DLR-007. See the [source map and shared completion rules](README.md).
