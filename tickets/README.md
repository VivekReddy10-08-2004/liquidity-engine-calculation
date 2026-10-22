# Implementation tickets

This directory breaks the proposal into reviewable pieces of work. It documents planned work; it does not claim those features are implemented.

## Current baseline

Already present: root uv project and lockfile, Python 3.12 environment configuration, backend dependencies and development tools, optional pgvector package, FastAPI `/health`, editor settings, and a PostgreSQL-only Compose file. Lint/type/dependency and API smoke checks passed during bootstrap. Docker was unavailable, so PostgreSQL/container startup remains unverified. There is no frontend, schema/migration set, liquidity engine, or product workflow yet.

## Release boundaries

- **Core MVP:** CORE-001 through CORE-023. Synthetic USD data, deterministic decisions, explanations, scenarios, policy versions, human decisions, audit history, and a reproducible local demo.
- **Optional hosting:** OPS-001. A separately selectable public portfolio deployment.
- **Optional RAG release:** AI-001 through AI-005. An evidence-based explanation assistant; not required to complete the core MVP.
- **Future AI enhancements:** AI-006 through AI-008. Daily brief, invoice draft review, and policy drafting; each is independently optional after its prerequisites.

The phase split is the proposed execution plan for this backlog. It makes the source document’s “optional AI” language explicit; it does not remove those features from the longer-term scope.

All work uses synthetic data. No ticket authorizes live integrations, money movement or transfer simulation, investment execution, multi-currency, or autonomous financial decisions.

## How to use these tickets

Start with CORE-001 to settle the documented contradictions. CORE-011 can also start immediately. Then take tickets whose dependencies are Done; independent branches may proceed concurrently. Dependencies describe required completed capabilities, not estimates or staffing assignments.

Statuses: **Ready** means no unfinished prerequisites at creation; **Backlog** means prerequisites remain; use **In progress**, **Blocked** (with a stated reason), and **Done** as work advances. All implementation tickets are unfinished. No owners or delivery dates have been invented.

Each ticket contains an outcome, bounded work, observable acceptance criteria, exclusions, and source references. Update its checkboxes/status and this index together. If a ticket grows beyond one coherent review, split it and preserve dependency links.

## Shared completion rules

- Complete the listed acceptance criteria and attach a brief verification note with relevant commands/results or manual evidence.
- Add meaningful tests with each behavioral change; CORE-022 integrates and extends them rather than postponing testing.
- Enforce server-side organization ownership and permissions wherever data is read or changed.
- Preserve decimal monetary values, input/policy/rules provenance, and applicable audit events.
- Update API/setup documentation when the change affects them; do not mark unavailable infrastructure checks as passed.
- Keep SQL, model details, and other implementation terminology out of user-facing product copy unless needed for a decision.

## Suggested build order

1. Settle business rules (001), define contracts (002), and establish the frontend shell (011).
2. Build storage/access/audit/imports (003–006) alongside pure calculations and fail-safes (007–008).
3. Persist recommendations (009), add demo edits (010), and deliver dashboard/explanation (012).
4. Build projection/timeline (013–014), policy workflows (015–016), and scenario workflows (017–018).
5. Finish decision controls and audit browsing (019–021).
6. Verify CI/end-to-end behavior and package the local demo (022–023).
7. Select hosting and/or optional AI work only after the core release is complete.

## Ticket index

| Ticket | Outcome | Release | Status | Depends on |
|---|---|---|---|---|
| [CORE-001](CORE-001-resolve-calculation-and-workflow-rules.md) | Resolve calculation and workflow rules | Core MVP | Ready | — |
| [CORE-002](CORE-002-define-domain-and-api-contracts.md) | Define domain and API contracts | Core MVP | Backlog | CORE-001 |
| [CORE-003](CORE-003-create-database-schema-and-migrations.md) | Create database schema and migrations | Core MVP | Backlog | CORE-002 |
| [CORE-004](CORE-004-add-demo-identity-and-organization-access-checks.md) | Add demo identity and organization access checks | Core MVP | Backlog | CORE-003 |
| [CORE-005](CORE-005-implement-append-only-audit-recording.md) | Implement append-only audit recording | Core MVP | Backlog | CORE-004 |
| [CORE-006](CORE-006-build-repeatable-synthetic-data-imports.md) | Build repeatable synthetic data imports | Core MVP | Backlog | CORE-005 |
| [CORE-007](CORE-007-calculate-cash-and-reserved-obligations.md) | Calculate cash and reserved obligations | Core MVP | Backlog | CORE-002 |
| [CORE-008](CORE-008-apply-freshness-rules-and-choose-recommendations.md) | Apply freshness rules and choose recommendations | Core MVP | Backlog | CORE-007 |
| [CORE-009](CORE-009-persist-recommendations-and-immutable-snapshots.md) | Persist recommendations and immutable snapshots | Core MVP | Backlog | CORE-003, CORE-005, CORE-008 |
| [CORE-010](CORE-010-add-invoice-corrections-and-demo-source-controls.md) | Add invoice corrections and demo source controls | Core MVP | Backlog | CORE-006, CORE-009 |
| [CORE-011](CORE-011-build-the-react-application-foundation.md) | Build the React application foundation | Core MVP | Ready | — |
| [CORE-012](CORE-012-build-the-dashboard-and-calculation-explanation.md) | Build the dashboard and calculation explanation | Core MVP | Backlog | CORE-009, CORE-010, CORE-011 |
| [CORE-013](CORE-013-implement-the-daily-liquidity-projection.md) | Implement the daily liquidity projection | Core MVP | Backlog | CORE-007, CORE-009 |
| [CORE-014](CORE-014-build-the-liquidity-timeline-view.md) | Build the liquidity timeline view | Core MVP | Backlog | CORE-011, CORE-013 |
| [CORE-015](CORE-015-implement-policy-preview-and-immutable-versions.md) | Implement policy preview and immutable versions | Core MVP | Backlog | CORE-005, CORE-009 |
| [CORE-016](CORE-016-build-the-policy-editor-and-version-comparison.md) | Build the policy editor and version comparison | Core MVP | Backlog | CORE-011, CORE-015 |
| [CORE-017](CORE-017-implement-deterministic-downside-scenarios.md) | Implement deterministic downside scenarios | Core MVP | Backlog | CORE-009, CORE-013 |
| [CORE-018](CORE-018-build-scenario-comparison-controls.md) | Build scenario comparison controls | Core MVP | Backlog | CORE-011, CORE-017 |
| [CORE-019](CORE-019-implement-recommendation-decisions-and-concurrency-checks.md) | Implement recommendation decisions and concurrency checks | Core MVP | Backlog | CORE-004, CORE-005, CORE-009, CORE-015 |
| [CORE-020](CORE-020-build-human-decision-controls.md) | Build human decision controls | Core MVP | Backlog | CORE-012, CORE-019 |
| [CORE-021](CORE-021-build-the-audit-history-api-and-screen.md) | Build the audit history API and screen | Core MVP | Backlog | CORE-005, CORE-011, CORE-019 |
| [CORE-022](CORE-022-verify-the-complete-mvp-and-automate-ci.md) | Verify the complete MVP and automate CI | Core MVP | Backlog | CORE-012, CORE-014, CORE-016, CORE-018, CORE-020, CORE-021 |
| [CORE-023](CORE-023-package-the-local-demo-and-project-handoff.md) | Package the local demo and project handoff | Core MVP | Backlog | CORE-022 |
| [OPS-001](OPS-001-publish-a-synthetic-portfolio-demo.md) | Publish a synthetic portfolio demo | Hosting | Backlog | CORE-023 |
| [AI-001](AI-001-configure-the-optional-ai-provider-boundary.md) | Configure the optional AI provider boundary | RAG | Backlog | CORE-023 |
| [AI-002](AI-002-index-versioned-knowledge-documents.md) | Index versioned knowledge documents | RAG | Backlog | AI-001, CORE-003 |
| [AI-003](AI-003-retrieve-authorized-evidence-for-a-recommendation.md) | Retrieve authorized evidence for a recommendation | RAG | Backlog | AI-002, CORE-009, CORE-021 |
| [AI-004](AI-004-build-cited-assistant-answers-and-query-audit.md) | Build cited assistant answers and query audit | RAG | Backlog | AI-003 |
| [AI-005](AI-005-build-the-assistant-panel-and-evaluation-gate.md) | Build the assistant panel and evaluation gate | RAG | Backlog | AI-004, CORE-012 |
| [AI-006](AI-006-generate-a-daily-treasury-brief.md) | Generate a daily treasury brief | Future AI | Backlog | AI-005 |
| [AI-007](AI-007-extract-invoice-drafts-for-human-review.md) | Extract invoice drafts for human review | Future AI | Backlog | AI-005, CORE-010 |
| [AI-008](AI-008-draft-policy-changes-from-natural-language.md) | Draft policy changes from natural language | Future AI | Backlog | AI-005, CORE-016 |

## Source map

Source documents retain their original proposal ticket IDs. The new CORE/AI/OPS IDs avoid the original collision where, for example, DLR-006 means scenarios in one document and RAG ingestion in another.

- [Original MVP specification](<../docs/dynamic-liquidity-reserve-mvp-ticket (1).md>)
- [Architecture diagrams](../docs/dynamic-liquidity-reserve-architecture.md)
- [RAG and extended architecture](../docs/dynamic-liquidity-reserve-rag-architecture.md)

| Original requirement | New tickets |
|---|---|
| Rules inconsistencies and decision semantics | CORE-001 |
| MVP DLR-001: contracts/imports | CORE-002–006 |
| MVP DLR-002: calculation engine | CORE-007–009 |
| MVP DLR-003 / FR-8: freshness | CORE-008, CORE-010, CORE-012 |
| MVP DLR-004 / FR-1, FR-2, FR-4: dashboard/explanation/timeline | CORE-009, CORE-011–014 |
| MVP DLR-005 / FR-3: policy versions | CORE-015–016 |
| MVP DLR-006 / FR-5: scenarios | CORE-017–018 |
| MVP DLR-007 / FR-6, FR-7: decisions/corrections/audit | CORE-005, CORE-010, CORE-019–021 |
| MVP DLR-008: verification/demo/deployment | CORE-022–023, OPS-001 |
| RAG DLR-001–005: core platform | CORE-001–021 |
| RAG DLR-006: ingestion/retrieval | AI-001–003 |
| RAG DLR-007: grounded assistant | AI-004–005 |
| RAG DLR-008: brief/extraction | AI-006–007 |
| RAG DLR-009: tests/evaluations/demo | CORE-022–023, OPS-001, AI-005 |
| RAG Phase 3: policy draft assistant | AI-008 |

## Decisions that must be settled first

CORE-001 owns the unresolved receivables/allocation relationship, overlapping reserve windows and pending-debit deduplication, buffer behavior in the invoice example, exact freshness thresholds/action precedence, and approvals after critical data blocks. Later tickets reference its resulting specification rather than inventing conflicting answers. The fixed 30-day view versus configurable policy horizon and authoritative generation versus dashboard GET behavior must also be documented there or in their designated service tickets.
