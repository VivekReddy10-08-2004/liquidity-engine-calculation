from collections.abc import Iterator
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.domain.enums import BufferStrategy
from backend.app.models import Organization, RecommendationSnapshot, TreasuryPolicy


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:  # type: ignore[no-untyped-def]
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine) as value:
        yield value


def make_policy(
    organization_id: UUID, *, policy_id: UUID | None = None, version: int = 1
) -> TreasuryPolicy:
    return TreasuryPolicy(
        id=policy_id or uuid4(),
        organization_id=organization_id,
        version=version,
        forecast_horizon_days=30,
        cash_floor_amount=Decimal("90000.00"),
        payroll_cycles_to_reserve=2,
        ap_reserve_window_days=30,
        fixed_uncertainty_buffer=Decimal("169000.00"),
        variable_buffer_percent=Decimal("20.0000"),
        buffer_strategy=BufferStrategy.MAXIMUM,
        approval_threshold=Decimal("1000000.00"),
        effective_at=datetime.now(UTC),
        created_by=uuid4(),
    )


def test_decimal_round_trip_is_exact(session: Session) -> None:
    org = Organization(name="Northstar Cloud")
    session.add(org)
    session.flush()
    policy = make_policy(org.id)
    session.add(policy)
    session.commit()
    session.refresh(policy)
    assert policy.cash_floor_amount == Decimal("90000.00")
    assert policy.variable_buffer_percent == Decimal("20.0000")


def test_cross_organization_policy_reference_is_rejected(session: Session) -> None:
    org_a = Organization(name="A")
    org_b = Organization(name="B")
    session.add_all([org_a, org_b])
    session.flush()
    policy = make_policy(org_a.id)
    session.add(policy)
    session.commit()
    snapshot = RecommendationSnapshot(
        organization_id=org_b.id,
        policy_id=policy.id,
        action="allocate",
        recommended_amount=Decimal("1.00"),
        required_liquidity=Decimal("1.00"),
        available_cash=Decimal("2.00"),
        confidence="high",
        input_snapshot={"test": True},
        rules_version="v1.0.0",
        generated_at=datetime.now(UTC),
        status="pending",
    )
    session.add(snapshot)
    with pytest.raises(IntegrityError):
        session.commit()


def test_policy_version_is_unique_per_organization(session: Session) -> None:
    org = Organization(name="A")
    session.add(org)
    session.flush()
    session.add_all([make_policy(org.id), make_policy(org.id)])
    with pytest.raises(IntegrityError):
        session.commit()
