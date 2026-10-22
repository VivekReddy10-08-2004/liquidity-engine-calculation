import csv
import json
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from backend.app.api.errors import validation_issues
from backend.app.schemas import (
    CashAccountCreate,
    DemoDataBundle,
    ObligationCreate,
    TreasuryPolicyCreate,
    UserDecisionCreate,
)

ORG_ID = UUID("10000000-0000-4000-8000-000000000001")
NOW = datetime(2026, 10, 21, 13, tzinfo=UTC)


def account_payload() -> dict[str, object]:
    return {
        "organization_id": str(ORG_ID),
        "name": "Primary Operating",
        "account_type": "operating",
        "currency": "USD",
        "available_balance": "2100000.10",
        "ledger_balance": "2100010.10",
        "as_of_at": "2026-10-21T13:00:00Z",
        "freshness": "fresh",
        "source_system": "demo_bank",
        "source_identifier": "acct-001",
        "source_version": "v1",
    }


def policy_payload() -> dict[str, object]:
    return {
        "id": "10000000-0000-4000-8000-000000000010",
        "organization_id": str(ORG_ID),
        "version": 1,
        "forecast_horizon_days": 30,
        "cash_floor_amount": "90000.00",
        "payroll_cycles_to_reserve": 2,
        "ap_reserve_window_days": 30,
        "fixed_uncertainty_buffer": "169000.00",
        "variable_buffer_percent": "20.0000",
        "buffer_strategy": "maximum",
        "approval_threshold": "1000000.00",
        "effective_at": NOW.isoformat(),
        "created_by": str(uuid4()),
    }


def test_money_remains_decimal_and_serializes_as_string() -> None:
    account = CashAccountCreate.model_validate(account_payload())
    assert account.available_balance == Decimal("2100000.10")
    assert account.model_dump(mode="json")["available_balance"] == "2100000.10"


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("available_balance", "-0.01", "negative_amount"),
        ("available_balance", 10.25, "money_float_not_allowed"),
        ("currency", "EUR", "unsupported_currency"),
        ("currency", 123, "string_type"),
        ("as_of_at", "not-a-date", "datetime_from_date_parsing"),
        ("source_identifier", "", "string_too_short"),
    ],
)
def test_invalid_account_payloads_have_structured_errors(
    field: str, value: object, error_type: str
) -> None:
    payload = account_payload()
    payload[field] = value
    with pytest.raises(ValidationError) as exc_info:
        CashAccountCreate.model_validate(payload)
    issue = validation_issues(exc_info.value.errors())[0]
    assert issue.code == error_type
    assert issue.field == field
    assert issue.message


def test_naive_timestamp_is_rejected() -> None:
    payload = account_payload()
    payload["as_of_at"] = "2026-10-21T13:00:00"
    with pytest.raises(ValidationError, match="timezone offset"):
        CashAccountCreate.model_validate(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("forecast_horizon_days", 31),
        ("payroll_cycles_to_reserve", 4),
        ("ap_reserve_window_days", 21),
    ],
)
def test_invalid_policy_ranges(field: str, value: int) -> None:
    payload = policy_payload()
    payload[field] = value
    with pytest.raises(ValidationError) as exc_info:
        TreasuryPolicyCreate.model_validate(
            {key: val for key, val in payload.items() if key != "id"}
        )
    assert exc_info.value.errors()[0]["type"] == "invalid_policy_range"


def test_obligation_date_and_amount_validation() -> None:
    payload = {
        "organization_id": str(ORG_ID),
        "obligation_type": "tax",
        "amount": "100.00",
        "currency": "USD",
        "due_date": date(2026, 10, 31).isoformat(),
        "certainty": "confirmed",
        "status": "scheduled",
        "source_system": "manual",
        "source_identifier": "tax-1",
        "source_version": "v1",
        "source_updated_at": NOW.isoformat(),
    }
    obligation = ObligationCreate.model_validate(payload)
    assert obligation.amount == Decimal("100.00")
    payload["due_date"] = "2026-02-30"
    with pytest.raises(ValidationError):
        ObligationCreate.model_validate(payload)


def test_override_requires_amount_and_reason() -> None:
    with pytest.raises(ValidationError, match="Approved amount is required"):
        UserDecisionCreate.model_validate(
            {
                "organization_id": str(ORG_ID),
                "recommendation_id": str(uuid4()),
                "decision": "override",
                "actor_id": str(uuid4()),
                "decided_at": NOW.isoformat(),
            }
        )


def test_demo_json_validates_before_import() -> None:
    path = Path(__file__).parents[2] / "demo_data" / "demo_bundle.json"
    bundle = DemoDataBundle.model_validate(json.loads(path.read_text()))
    assert bundle.organization_id == ORG_ID
    assert bundle.accounts[0].available_balance == Decimal("2100000.00")


def test_demo_csv_rows_validate_before_import() -> None:
    directory = Path(__file__).parents[2] / "demo_data"
    with (directory / "accounts.csv").open(newline="") as file:
        accounts = [CashAccountCreate.model_validate(row) for row in csv.DictReader(file)]
    with (directory / "obligations.csv").open(newline="") as file:
        obligations = [ObligationCreate.model_validate(row) for row in csv.DictReader(file)]
    assert accounts[0].available_balance == Decimal("2100000.00")
    assert obligations[0].amount == Decimal("360000.00")


def test_demo_bundle_rejects_cross_tenant_record() -> None:
    payload = {
        "organization_id": str(ORG_ID),
        "accounts": [{**account_payload(), "organization_id": str(uuid4())}],
        "obligations": [],
        "policies": [policy_payload()],
    }
    with pytest.raises(ValidationError) as exc_info:
        DemoDataBundle.model_validate(payload)
    assert exc_info.value.errors()[0]["type"] == "organization_mismatch"
