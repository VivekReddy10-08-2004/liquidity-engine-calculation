"""Create the tenant-scoped cash-domain contract tables.

Revision ID: 20261021_0001
Revises: None
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261021_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _enum(name: str, values: list[str]) -> sa.Enum:
    return sa.Enum(*values, name=name, native_enum=False, create_constraint=True)


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="pk_organizations"),
    )
    op.create_table(
        "cash_accounts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column(
            "account_type",
            _enum("account_type", ["operating", "treasury_reserve", "restricted"]),
            nullable=False,
        ),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("available_balance", sa.Numeric(20, 2), nullable=False),
        sa.Column("ledger_balance", sa.Numeric(20, 2), nullable=False),
        sa.Column("as_of_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "freshness", _enum("freshness", ["fresh", "warning", "stale", "error"]), nullable=False
        ),
        sa.Column("source_system", sa.String(100), nullable=False),
        sa.Column("source_identifier", sa.String(255), nullable=False),
        sa.Column("source_version", sa.String(100), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("currency = 'USD'", name="currency_usd"),
        sa.CheckConstraint("available_balance >= 0", name="available_balance_nonnegative"),
        sa.CheckConstraint("ledger_balance >= 0", name="ledger_balance_nonnegative"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_cash_accounts_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_cash_accounts"),
        sa.UniqueConstraint("id", "organization_id", name="uq_cash_accounts_id_org"),
        sa.UniqueConstraint(
            "organization_id",
            "source_system",
            "source_identifier",
            "source_version",
            name="uq_cash_accounts_source_version",
        ),
    )
    op.create_index("ix_cash_accounts_organization_id", "cash_accounts", ["organization_id"])
    op.create_table(
        "obligations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column(
            "obligation_type",
            _enum(
                "obligation_type",
                [
                    "payroll",
                    "tax",
                    "accounts_payable",
                    "card_settlement",
                    "debt",
                    "subscription",
                    "other",
                ],
            ),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column(
            "certainty",
            _enum("obligation_certainty", ["confirmed", "expected", "uncertain"]),
            nullable=False,
        ),
        sa.Column(
            "status",
            _enum("transaction_status", ["scheduled", "pending", "paid", "canceled"]),
            nullable=False,
        ),
        sa.Column("source_system", sa.String(100), nullable=False),
        sa.Column("source_identifier", sa.String(255), nullable=False),
        sa.Column("source_version", sa.String(100), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("included_in_reserve", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("currency = 'USD'", name="currency_usd"),
        sa.CheckConstraint("amount >= 0", name="amount_nonnegative"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_obligations_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_obligations"),
        sa.UniqueConstraint("id", "organization_id", name="uq_obligations_id_org"),
        sa.UniqueConstraint(
            "organization_id",
            "source_system",
            "source_identifier",
            "source_version",
            name="uq_obligations_source_version",
        ),
    )
    op.create_index("ix_obligations_organization_id", "obligations", ["organization_id"])
    op.create_index("ix_obligations_org_due_date", "obligations", ["organization_id", "due_date"])
    op.create_table(
        "treasury_policies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("forecast_horizon_days", sa.Integer(), nullable=False),
        sa.Column("cash_floor_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("payroll_cycles_to_reserve", sa.Integer(), nullable=False),
        sa.Column("ap_reserve_window_days", sa.Integer(), nullable=False),
        sa.Column("fixed_uncertainty_buffer", sa.Numeric(20, 2), nullable=False),
        sa.Column("variable_buffer_percent", sa.Numeric(7, 4), nullable=False),
        sa.Column(
            "buffer_strategy",
            _enum("buffer_strategy", ["fixed", "percentage", "maximum"]),
            nullable=False,
        ),
        sa.Column("approval_threshold", sa.Numeric(20, 2), nullable=False),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            "forecast_horizon_days IN (7, 14, 30, 45, 60)",
            name="valid_horizon",
        ),
        sa.CheckConstraint(
            "payroll_cycles_to_reserve BETWEEN 1 AND 3",
            name="valid_payroll_cycles",
        ),
        sa.CheckConstraint("ap_reserve_window_days IN (7, 14, 30)", name="valid_ap_window"),
        sa.CheckConstraint("cash_floor_amount >= 0", name="cash_floor_nonnegative"),
        sa.CheckConstraint("fixed_uncertainty_buffer >= 0", name="fixed_buffer_nonnegative"),
        sa.CheckConstraint(
            "variable_buffer_percent BETWEEN 0 AND 100",
            name="variable_buffer_percent_range",
        ),
        sa.CheckConstraint("approval_threshold >= 0", name="approval_threshold_nonnegative"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_treasury_policies_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_treasury_policies"),
        sa.UniqueConstraint("id", "organization_id", name="uq_treasury_policies_id_org"),
        sa.UniqueConstraint("organization_id", "version", name="uq_treasury_policies_org_version"),
    )
    op.create_index(
        "ix_treasury_policies_organization_id", "treasury_policies", ["organization_id"]
    )
    op.create_index(
        "ix_treasury_policies_org_effective",
        "treasury_policies",
        ["organization_id", "effective_at"],
    )
    op.create_table(
        "recommendation_snapshots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("policy_id", sa.Uuid(), nullable=False),
        sa.Column(
            "action",
            _enum("recommendation_action", ["allocate", "hold", "pull_back", "review_required"]),
            nullable=False,
        ),
        sa.Column("recommended_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("required_liquidity", sa.Numeric(20, 2), nullable=False),
        sa.Column("available_cash", sa.Numeric(20, 2), nullable=False),
        sa.Column("confidence", _enum("confidence", ["high", "medium", "low"]), nullable=False),
        sa.Column("input_snapshot", sa.JSON(), nullable=False),
        sa.Column("rules_version", sa.String(50), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            _enum(
                "recommendation_status",
                ["pending", "approved", "rejected", "deferred", "superseded"],
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            "recommended_amount >= 0",
            name="recommended_amount_nonnegative",
        ),
        sa.CheckConstraint(
            "required_liquidity >= 0",
            name="required_liquidity_nonnegative",
        ),
        sa.CheckConstraint("available_cash >= 0", name="available_cash_nonnegative"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_recommendation_snapshots_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["policy_id", "organization_id"],
            ["treasury_policies.id", "treasury_policies.organization_id"],
            name="fk_recommendation_snapshots_policy_id_treasury_policies",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_recommendation_snapshots"),
        sa.UniqueConstraint("id", "organization_id", name="uq_recommendation_snapshots_id_org"),
    )
    op.create_index(
        "ix_recommendation_snapshots_organization_id",
        "recommendation_snapshots",
        ["organization_id"],
    )
    op.create_index(
        "ix_recommendation_snapshots_org_generated",
        "recommendation_snapshots",
        ["organization_id", "generated_at"],
    )
    op.create_table(
        "user_decisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("recommendation_id", sa.Uuid(), nullable=False),
        sa.Column(
            "decision",
            _enum("decision_action", ["approve", "reject", "defer", "override"]),
            nullable=False,
        ),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("approved_amount", sa.Numeric(20, 2), nullable=True),
        sa.Column("reason", sa.String(1000), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            "approved_amount IS NULL OR approved_amount >= 0",
            name="amount_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_user_decisions_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["recommendation_id", "organization_id"],
            ["recommendation_snapshots.id", "recommendation_snapshots.organization_id"],
            name="fk_user_decisions_recommendation_id_recommendation_snapshots",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_decisions"),
        sa.UniqueConstraint("id", "organization_id", name="uq_user_decisions_id_org"),
    )
    op.create_index("ix_user_decisions_organization_id", "user_decisions", ["organization_id"])
    op.create_index(
        "ix_user_decisions_org_decided", "user_decisions", ["organization_id", "decided_at"]
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_audit_events_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_audit_events"),
        sa.UniqueConstraint("id", "organization_id", name="uq_audit_events_id_org"),
    )
    op.create_index("ix_audit_events_organization_id", "audit_events", ["organization_id"])
    op.create_index(
        "ix_audit_events_org_occurred", "audit_events", ["organization_id", "occurred_at"]
    )
    op.create_index(
        "ix_audit_events_org_entity",
        "audit_events",
        ["organization_id", "entity_type", "entity_id"],
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("user_decisions")
    op.drop_table("recommendation_snapshots")
    op.drop_table("treasury_policies")
    op.drop_table("obligations")
    op.drop_table("cash_accounts")
    op.drop_table("organizations")
