# AI-001 — Configure the optional AI provider boundary

**Status:** Backlog  
**Release:** Optional RAG release  
**Depends on:** [CORE-023](CORE-023-package-the-local-demo-and-project-handoff.md)

## Outcome

Introduce an opt-in provider adapter without making the core product depend on AI.

## Work to do

- Select one structured-output/embedding provider and document model configuration, credentials, timeouts, and usage limits.
- Create a provider adapter, feature flag, fake test implementation, and schema-validated response contract.
- Separate financial read access from application-owned AI audit writes; expose no general SQL or mutation tools to the model.

## Acceptance criteria

- [ ] The entire core demo works with AI disabled and no provider credentials.
- [ ] Missing credentials, timeout, and provider errors return controlled assistant-unavailable states.
- [ ] Secrets are loaded from environment and omitted from logs; synthetic evidence is the only supported input.
- [ ] Tests use the fake adapter by default; document separately how to run an optional live-provider smoke check.

## Out of scope

No assistant UI or financial calculations by an LLM.

## Source requirements

RAG: Product Principles, Technical Stack, Access control. See the [source map and shared completion rules](README.md).
