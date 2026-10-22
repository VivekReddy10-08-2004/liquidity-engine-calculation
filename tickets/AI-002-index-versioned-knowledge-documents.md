# AI-002 — Index versioned knowledge documents

**Status:** Backlog  
**Release:** Optional RAG release  
**Depends on:** [AI-001](AI-001-configure-the-optional-ai-provider-boundary.md), [CORE-003](CORE-003-create-database-schema-and-migrations.md)

## Outcome

Make controlled narrative sources searchable with provenance and tenant ownership.

## Work to do

- Enable pgvector through a migration and create knowledge_documents/knowledge_chunks tables with embedding configuration.
- Normalize, chunk, embed, and index controlled policy/glossary/scenario docs and immutable snapshot summaries.
- Add admin-only reindexing with content hashes, lifecycle metadata, and explicit global-document allowlisting.

## Acceptance criteria

- [ ] Reindexing unchanged content produces no duplicate active chunks.
- [ ] Each chunk identifies its source, organization or approved global scope, and applicable snapshot/policy/rules version.
- [ ] Superseded documents cannot silently replace historical evidence.
- [ ] Migration/indexing tests cover changed content, provider failure, and unauthorized reindex requests.

## Out of scope

No unrestricted web ingestion or raw private document indexing.

## Source requirements

RAG: Retrieval Design, Data Model Additions, DLR-006. See the [source map and shared completion rules](README.md).
