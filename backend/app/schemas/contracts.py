"""Normalized request, response, and demo-import contracts for DLR-001."""

from datetime import date, datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import Field, StringConstraints, field_validator, model_validator
from pydantic_core import PydanticCustomError

from backend.app.domain.enums import (
    AccountType,
    BufferStrategy,
    Confidence,
    DecisionAction,
    Freshness,
    ObligationCertainty,
    ObligationType,
    RecommendationAction,
    RecommendationStatus,
    TransactionStatus,
)
from backend.app.schemas.base import (
    ContractModel,
    Money,
    Percentage,
    parse_money,
    validate_currency,
    validate_utc,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TenantContract(ContractModel):
    organization_id: UUID


class SourceContract(ContractModel):
    source_system: NonEmptyString
    source_identifier: NonEmptyString
    source_version: NonEmptyString


class CashAccountCreate(TenantContract, SourceContract):
    name: NonEmptyString
    account_type: AccountType
    currency: str = "USD"
    available_balance: Money
    ledger_balance: Money
    as_of_at: datetime
    freshness: Freshness

    _currency = field_validator("currency", mode="before")(validate_currency)
    _amounts = field_validator("available_balance", "ledger_balance", mode="before")(parse_money)
    _as_of_at = field_validator("as_of_at")(validate_utc)


class CashAccountResponse(CashAccountCreate):
    id: UUID
    created_at: datetime

    _created_at = field_validator("created_at")(validate_utc)


class ObligationCreate(TenantContract, SourceContract):
    obligation_type: ObligationType
    amount: Money
    currency: str = "USD"
    due_date: date
    certainty: ObligationCertainty
    status: TransactionStatus
    source_updated_at: datetime
    included_in_reserve: bool = True
    description: str | None = Field(default=None, max_length=500)

    _currency = field_validator("currency", mode="before")(validate_currency)
    _amount = field_validator("amount", mode="before")(parse_money)
    _source_updated_at = field_validator("source_updated_at")(validate_utc)


class ObligationResponse(ObligationCreate):
    id: UUID
    created_at: datetime

    _created_at = field_validator("created_at")(validate_utc)


class TreasuryPolicyCreate(TenantContract):
    version: Annotated[int, Field(ge=1)]
    forecast_horizon_days: int
    cash_floor_amount: Money
    payroll_cycles_to_reserve: int
    ap_reserve_window_days: int
    fixed_uncertainty_buffer: Money
    variable_buffer_percent: Percentage
    buffer_strategy: BufferStrategy = BufferStrategy.MAXIMUM
    approval_threshold: Money
    effective_at: datetime
    created_by: UUID

    _amounts = field_validator(
        "cash_floor_amount",
        "fixed_uncertainty_buffer",
        "approval_threshold",
        mode="before",
    )(parse_money)
    _effective_at = field_validator("effective_at")(validate_utc)

    @field_validator("forecast_horizon_days")
    @classmethod
    def valid_horizon(cls, value: int) -> int:
        if value not in {7, 14, 30, 45, 60}:
            raise PydanticCustomError(
                "invalid_policy_range",
                "Forecast horizon must be one of 7, 14, 30, 45, or 60 days",
                {"allowed": [7, 14, 30, 45, 60]},
            )
        return value

    @field_validator("payroll_cycles_to_reserve")
    @classmethod
    def valid_payroll_cycles(cls, value: int) -> int:
        if value not in {1, 2, 3}:
            raise PydanticCustomError(
                "invalid_policy_range",
                "Payroll coverage must be one, two, or three cycles",
                {"minimum": 1, "maximum": 3},
            )
        return value

    @field_validator("ap_reserve_window_days")
    @classmethod
    def valid_ap_window(cls, value: int) -> int:
        if value not in {7, 14, 30}:
            raise PydanticCustomError(
                "invalid_policy_range",
                "AP reserve window must be one of 7, 14, or 30 days",
                {"allowed": [7, 14, 30]},
            )
        return value


class TreasuryPolicyResponse(TreasuryPolicyCreate):
    id: UUID
    created_at: datetime

    _created_at = field_validator("created_at")(validate_utc)


class DemoTreasuryPolicy(TreasuryPolicyCreate):
    """Import policy with a stable ID for snapshot references."""

    id: UUID


class RecommendationSnapshotCreate(TenantContract):
    policy_id: UUID
    action: RecommendationAction
    recommended_amount: Money
    required_liquidity: Money
    available_cash: Money
    confidence: Confidence
    input_snapshot: dict[str, Any]
    rules_version: NonEmptyString
    generated_at: datetime
    status: RecommendationStatus = RecommendationStatus.PENDING

    _amounts = field_validator(
        "recommended_amount", "required_liquidity", "available_cash", mode="before"
    )(parse_money)
    _generated_at = field_validator("generated_at")(validate_utc)

    @field_validator("input_snapshot")
    @classmethod
    def nonempty_snapshot(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("Input snapshot must contain the recommendation inputs")
        return value


class RecommendationSnapshotResponse(RecommendationSnapshotCreate):
    id: UUID
    created_at: datetime

    _created_at = field_validator("created_at")(validate_utc)


class UserDecisionCreate(TenantContract):
    recommendation_id: UUID
    decision: DecisionAction
    actor_id: UUID
    approved_amount: Money | None = None
    reason: str | None = Field(default=None, max_length=1000)
    decided_at: datetime

    _approved_amount = field_validator("approved_amount", mode="before")(parse_money)
    _decided_at = field_validator("decided_at")(validate_utc)

    @model_validator(mode="after")
    def validate_decision_details(self) -> "UserDecisionCreate":
        if self.decision in {DecisionAction.APPROVE, DecisionAction.OVERRIDE}:
            if self.approved_amount is None:
                raise ValueError("Approved amount is required for approve and override decisions")
        elif self.approved_amount is not None:
            raise ValueError("Approved amount is only valid for approve and override decisions")
        if self.decision == DecisionAction.OVERRIDE and not (self.reason or "").strip():
            raise ValueError("A user-readable reason is required for an override")
        return self


class UserDecisionResponse(UserDecisionCreate):
    id: UUID
    created_at: datetime

    _created_at = field_validator("created_at")(validate_utc)


class AuditEventCreate(TenantContract):
    entity_type: NonEmptyString
    entity_id: UUID
    event_type: NonEmptyString
    actor_id: UUID | None = None
    payload: dict[str, Any]
    occurred_at: datetime

    _occurred_at = field_validator("occurred_at")(validate_utc)


class AuditEventResponse(AuditEventCreate):
    id: UUID


class DemoDataBundle(TenantContract):
    """Atomic JSON import format; all nested rows must belong to the bundle tenant."""

    accounts: list[CashAccountCreate]
    obligations: list[ObligationCreate]
    policies: list[DemoTreasuryPolicy]
    recommendation_snapshots: list[RecommendationSnapshotCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_single_tenant(self) -> "DemoDataBundle":
        nested = [
            *self.accounts,
            *self.obligations,
            *self.policies,
            *self.recommendation_snapshots,
        ]
        mismatches = [
            str(row.organization_id)
            for row in nested
            if row.organization_id != self.organization_id
        ]
        if mismatches:
            raise PydanticCustomError(
                "organization_mismatch",
                "Every demo record must match the bundle organization_id",
                {"mismatched_organization_ids": sorted(set(mismatches))},
            )
        policy_ids = {policy.id for policy in self.policies}
        missing_policy_ids = sorted(
            str(snapshot.policy_id)
            for snapshot in self.recommendation_snapshots
            if snapshot.policy_id not in policy_ids
        )
        if missing_policy_ids:
            raise PydanticCustomError(
                "invalid_reference",
                "Every recommendation snapshot must reference a policy in the demo bundle",
                {"missing_policy_ids": missing_policy_ids},
            )
        return self
