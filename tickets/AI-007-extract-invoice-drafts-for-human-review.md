# AI-007 — Extract invoice drafts for human review

**Status:** Backlog  
**Release:** Future AI enhancement  
**Depends on:** [AI-005](AI-005-build-the-assistant-panel-and-evaluation-gate.md), [CORE-010](CORE-010-add-invoice-corrections-and-demo-source-controls.md)

## Outcome

Turn a synthetic invoice into a reviewable draft before creating an obligation.

## Work to do

- Support bounded synthetic text/PDF uploads with explicit type/size limits and a structured extraction schema.
- Add a review queue showing source document, extracted fields, validation errors, confidence, and editable draft values.
- Only explicit authorized confirmation sends a validated record through the normal obligation/import pipeline.

## Acceptance criteria

- [ ] Extraction alone creates no authoritative obligation.
- [ ] Invalid amounts/dates/currency and duplicates are flagged before confirmation.
- [ ] Confirmation is retry-safe and records source, extraction version/output, reviewer changes, and final obligation reference.
- [ ] Tests cover malicious document instructions, malformed files, provider failure, rejection, and duplicate confirmation.

## Out of scope

No OCR promise for scanned PDFs unless separately scoped; no auto-approval or vendor payment.

## Source requirements

RAG: Phase 2B and DLR-008. See the [source map and shared completion rules](README.md).
