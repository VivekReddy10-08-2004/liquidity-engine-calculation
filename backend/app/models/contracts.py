"""Tenant-scoped persistence models for DLR-001."""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PythonEnum
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base
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

MONEY = Numeric(20, 2)
PERCENTAGE = Numeric(7, 4)


def enum_column(enum_type: type[PythonEnum], name: str) -> Enum:
    return Enum(
        enum_type,
        name=name,
        native_enum=False,
        create_constraint=True,
        validate_strings=True,
        values_callable=lambda members: [member.value for member in members],
    )


class TenantIdMixin:
    organization_id: Mapped[UUID] = mapped_column(index=True, nullable=False)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Organization(Base):
    """Tenant root; its primary key is the organization scope identifier."""

    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class CashAccount(TenantIdMixin, TimestampMixin, Base):
    __tablename__ = "cash_accounts"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        UniqueConstraint("id", "organization_id", name="uq_cash_accounts_id_org"),
        UniqueConstraint(
            "organization_id",
            "source_system",
            "source_identifier",
            "source_version",
            name="uq_cash_accounts_source_version",
        ),
        CheckConstraint("currency = 'USD'", name="currency_usd"),
        CheckConstraint("available_balance >= 0", name="available_balance_nonnegative"),
        CheckConstraint("ledger_balance >= 0", name="ledger_balance_nonnegative"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(
        enum_column(AccountType, "account_type"), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    available_balance: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    ledger_balance: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    as_of_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    freshness: Mapped[Freshness] = mapped_column(
        enum_column(Freshness, "freshness"), nullable=False
    )
    source_system: Mapped[str] = mapped_column(String(100), nullable=False)
    source_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    source_version: Mapped[str] = mapped_column(String(100), nullable=False)


class Obligation(TenantIdMixin, TimestampMixin, Base):
    __tablename__ = "obligations"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        UniqueConstraint("id", "organization_id", name="uq_obligations_id_org"),
        UniqueConstraint(
            "organization_id",
            "source_system",
            "source_identifier",
            "source_version",
            name="uq_obligations_source_version",
        ),
        CheckConstraint("currency = 'USD'", name="currency_usd"),
        CheckConstraint("amount >= 0", name="amount_nonnegative"),
        Index("ix_obligations_org_due_date", "organization_id", "due_date"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    obligation_type: Mapped[ObligationType] = mapped_column(
        enum_column(ObligationType, "obligation_type"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    certainty: Mapped[ObligationCertainty] = mapped_column(
        enum_column(ObligationCertainty, "obligation_certainty"), nullable=False
    )
    status: Mapped[TransactionStatus] = mapped_column(
        enum_column(TransactionStatus, "transaction_status"), nullable=False
    )
    source_system: Mapped[str] = mapped_column(String(100), nullable=False)
    source_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    source_version: Mapped[str] = mapped_column(String(100), nullable=False)
    source_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    included_in_reserve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String(500))


class TreasuryPolicy(TenantIdMixin, TimestampMixin, Base):
    __tablename__ = "treasury_policies"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        UniqueConstraint("id", "organization_id", name="uq_treasury_policies_id_org"),
        UniqueConstraint("organization_id", "version", name="uq_treasury_policies_org_version"),
        CheckConstraint("forecast_horizon_days IN (7, 14, 30, 45, 60)", name="valid_horizon"),
        CheckConstraint("payroll_cycles_to_reserve BETWEEN 1 AND 3", name="valid_payroll_cycles"),
        CheckConstraint("ap_reserve_window_days IN (7, 14, 30)", name="valid_ap_window"),
        CheckConstraint("cash_floor_amount >= 0", name="cash_floor_nonnegative"),
        CheckConstraint("fixed_uncertainty_buffer >= 0", name="fixed_buffer_nonnegative"),
        CheckConstraint(
            "variable_buffer_percent BETWEEN 0 AND 100", name="variable_buffer_percent_range"
        ),
        CheckConstraint("approval_threshold >= 0", name="approval_threshold_nonnegative"),
        Index("ix_treasury_policies_org_effective", "organization_id", "effective_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)
    cash_floor_amount: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    payroll_cycles_to_reserve: Mapped[int] = mapped_column(Integer, nullable=False)
    ap_reserve_window_days: Mapped[int] = mapped_column(Integer, nullable=False)
    fixed_uncertainty_buffer: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    variable_buffer_percent: Mapped[Decimal] = mapped_column(PERCENTAGE, nullable=False)
    buffer_strategy: Mapped[BufferStrategy] = mapped_column(
        enum_column(BufferStrategy, "buffer_strategy"), nullable=False
    )
    approval_threshold: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    effective_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[UUID] = mapped_column(nullable=False)


class RecommendationSnapshot(TenantIdMixin, TimestampMixin, Base):
    __tablename__ = "recommendation_snapshots"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        ForeignKeyConstraint(
            ["policy_id", "organization_id"],
            ["treasury_policies.id", "treasury_policies.organization_id"],
            ondelete="RESTRICT",
        ),
        UniqueConstraint("id", "organization_id", name="uq_recommendation_snapshots_id_org"),
        CheckConstraint("recommended_amount >= 0", name="recommended_amount_nonnegative"),
        CheckConstraint("required_liquidity >= 0", name="required_liquidity_nonnegative"),
        CheckConstraint("available_cash >= 0", name="available_cash_nonnegative"),
        Index("ix_recommendation_snapshots_org_generated", "organization_id", "generated_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    policy_id: Mapped[UUID] = mapped_column(nullable=False)
    action: Mapped[RecommendationAction] = mapped_column(
        enum_column(RecommendationAction, "recommendation_action"), nullable=False
    )
    recommended_amount: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    required_liquidity: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    available_cash: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    confidence: Mapped[Confidence] = mapped_column(
        enum_column(Confidence, "confidence"), nullable=False
    )
    input_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    rules_version: Mapped[str] = mapped_column(String(50), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[RecommendationStatus] = mapped_column(
        enum_column(RecommendationStatus, "recommendation_status"), nullable=False
    )


class UserDecision(TenantIdMixin, TimestampMixin, Base):
    __tablename__ = "user_decisions"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        ForeignKeyConstraint(
            ["recommendation_id", "organization_id"],
            ["recommendation_snapshots.id", "recommendation_snapshots.organization_id"],
            ondelete="RESTRICT",
        ),
        UniqueConstraint("id", "organization_id", name="uq_user_decisions_id_org"),
        CheckConstraint(
            "approved_amount IS NULL OR approved_amount >= 0", name="amount_nonnegative"
        ),
        Index("ix_user_decisions_org_decided", "organization_id", "decided_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    recommendation_id: Mapped[UUID] = mapped_column(nullable=False)
    decision: Mapped[DecisionAction] = mapped_column(
        enum_column(DecisionAction, "decision_action"), nullable=False
    )
    actor_id: Mapped[UUID] = mapped_column(nullable=False)
    approved_amount: Mapped[Decimal | None] = mapped_column(MONEY)
    reason: Mapped[str | None] = mapped_column(String(1000))
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AuditEvent(TenantIdMixin, Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        UniqueConstraint("id", "organization_id", name="uq_audit_events_id_org"),
        Index("ix_audit_events_org_occurred", "organization_id", "occurred_at"),
        Index("ix_audit_events_org_entity", "organization_id", "entity_type", "entity_id"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    actor_id: Mapped[UUID | None] = mapped_column()
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
