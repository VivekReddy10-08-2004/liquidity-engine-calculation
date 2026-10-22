# CORE-016 — Build the policy editor and version comparison

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-011](CORE-011-build-the-react-application-foundation.md), [CORE-015](CORE-015-implement-policy-preview-and-immutable-versions.md)

## Outcome

Let finance users understand a policy change before saving it.

## Work to do

- Create validated fields for every supported policy setting and human-readable explanations.
- Show preview amount/action, field-level changes, version history, and current-versus-prior comparison.
- Handle permissions, stale preview context, save conflicts, and backend validation errors.

## Acceptance criteria

- [ ] A cash-floor or horizon edit produces a preview and then a new saved version.
- [ ] Canceling leaves current policy and recommendation unchanged.
- [ ] The UI never represents a historical policy as editable.
- [ ] UI checks cover validation, read-only roles, failed saves, and successful version creation.

## Out of scope

No AI-generated policy fields.

## Source requirements

MVP: FR-3, DLR-005. See the [source map and shared completion rules](README.md).
