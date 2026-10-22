# AI-003 — Retrieve authorized evidence for a recommendation

**Status:** Backlog  
**Release:** Optional RAG release  
**Depends on:** [AI-002](AI-002-index-versioned-knowledge-documents.md), [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md), [CORE-021](CORE-021-build-the-audit-history-api-and-screen.md)

## Outcome

Supply exact financial facts and relevant documents for the selected recommendation.

## Work to do

- Build allowlisted SQL retrieval for facts and hybrid full-text/vector retrieval for narrative context.
- Apply organization, authorization, recommendation/version, and document-type constraints before ranking.
- Build a bounded evidence pack with stable source IDs, exact decimal values, and explicitly authorized prior snapshots for comparisons.

## Acceptance criteria

- [ ] Two-organization tests prove no cross-tenant evidence enters the pack.
- [ ] Historical questions retrieve matching historical policy/snapshot context.
- [ ] Missing prior evidence yields an explicit insufficient-evidence result rather than an invented change explanation.
- [ ] Tests assert numeric facts come from structured records and that retrieved text cannot choose identities or broaden scope.

## Out of scope

No answer generation or unrestricted database queries.

## Source requirements

RAG: Retrieval Design and RAG request flow. See the [source map and shared completion rules](README.md).
