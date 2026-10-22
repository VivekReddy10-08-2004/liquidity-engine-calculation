# CORE-001 — Resolve calculation and workflow rules

**Status:** Ready  
**Release:** Core MVP  
**Depends on:** None

## Outcome

Give implementers one unambiguous specification before building the engine.

## Work to do

- Write docs/decision-engine.md with formulas, worked examples, rounding, date boundaries, and an ordered action-selection table.
- Resolve receivables: the current formula uses cleared cash, but the delayed-revenue example lowers allocation. Record whether receipts affect only the timeline or also allocation, and update conflicting examples.
- Define precedence for horizon, payroll-cycle coverage, AP window, and floor; define how pending debits and linked obligations avoid double counting.
- Define freshness thresholds, confidence mapping, stale AP retention, approval eligibility after a data block, override limits, and supersession rules.

## Acceptance criteria

- [ ] Every documented input combination maps to exactly one action and amount; equality and insufficient reserve have examples.
- [ ] The base example reconciles to $1M required liquidity and $1.1M allocation. The $180K invoice example states why the buffer does or does not change.
- [ ] Revenue-delay examples follow the chosen rule rather than an unexplained $360K adjustment.
- [ ] Record decisions and update the conflicting source sections; list any unresolved decision as a blocker for its dependent ticket.

## Out of scope

No application implementation. Suggested resolutions are not approved business rules until recorded in this ticket’s deliverable.

## Source requirements

MVP: Core Decision Rules, FR-3–FR-6; RAG: Core Calculation and Demo Script. See the [source map and shared completion rules](README.md).
