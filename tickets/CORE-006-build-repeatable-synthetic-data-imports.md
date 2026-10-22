# CORE-006 — Build repeatable synthetic data imports

**Status:** Backlog  
**Release:** Core MVP  
**Depends on:** [CORE-005](CORE-005-implement-append-only-audit-recording.md)

## Outcome

Load Northstar Cloud and supported CSV files without duplicating obligations.

## Work to do

- Create demo-data files for accounts, payroll, AP, cards, taxes, receivables, source health, and policies.
- Implement POST /api/v1/imports/demo-company and POST /api/v1/imports/csv with shared normalization and validation.
- Use a controlled demo as-of date, stable source/version identifiers, and atomic import behavior; include fixtures for all four recommendation states.

## Acceptance criteria

- [ ] The base fixture has $2.1M operating cash, $850K reserve, and the documented $1M required-liquidity components.
- [ ] Importing identical records twice creates no duplicate financial rows; changed versions follow a documented update rule.
- [ ] Invalid files return row/field errors and do not partially alter financial data.
- [ ] Fixtures remain deterministic over time, and successful imports create audit events.

## Out of scope

No live integrations, arbitrary spreadsheet formats, or invoice-document extraction.

## Source requirements

MVP: Scope, Example Calculation, DLR-001, Demo Scenario. See the [source map and shared completion rules](README.md).
