# CORE-018 — Build scenario comparison controls

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-011](CORE-011-build-the-react-application-foundation.md), [CORE-017](CORE-017-implement-deterministic-downside-scenarios.md)

## Outcome

Make scenario assumptions and differences understandable side by side.

## Work to do

- Add scenario selection and comparison chart/table for the chosen recommendation.
- Show changed inputs, allocation delta, action, warnings, daily low point, and conservative reference.
- Keep base/scenario identifiers visible and handle a superseded base snapshot clearly.

## Acceptance criteria

- [ ] Users can compare all documented scenario types against the same base.
- [ ] An unchanged allocation is shown honestly with its reason; forecasts are clearly labeled.
- [ ] Running a scenario does not replace the dashboard’s authoritative base result.
- [ ] UI checks cover failed requests, blocked results, and consistent currency formatting.

## Out of scope

No approving a scenario as if it were a current base recommendation.

## Source requirements

MVP: FR-5. See the [source map and shared completion rules](README.md).
