"""Validation primitives used by every cash-domain contract."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic_core import PydanticCustomError

Money = Annotated[Decimal, Field(ge=Decimal("0"), max_digits=20, decimal_places=2)]
Percentage = Annotated[Decimal, Field(ge=Decimal("0"), le=Decimal("100"), decimal_places=4)]


def parse_money(value: Any) -> Any:
    """Reject binary floats and provide a domain-specific negative-money error."""
    if isinstance(value, float):
        raise PydanticCustomError(
            "money_float_not_allowed",
            "Money must be supplied as a decimal string, not a floating-point number",
        )
    try:
        decimal_value = Decimal(str(value))
    except Exception:
        return value
    if not decimal_value.is_finite():
        raise PydanticCustomError("invalid_amount", "Amount must be a finite decimal value")
    if decimal_value < 0:
        raise PydanticCustomError("negative_amount", "Amount must be zero or greater")
    return value


def validate_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise PydanticCustomError("timezone_required", "Timestamp must include a timezone offset")
    return value.astimezone(UTC)


def validate_currency(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    normalized = value.upper().strip()
    if normalized != "USD":
        raise PydanticCustomError(
            "unsupported_currency",
            "Only USD is supported in the MVP",
            {"supported": ["USD"]},
        )
    return normalized


class ContractModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid", from_attributes=True, populate_by_name=True, validate_assignment=True
    )

    @field_serializer("*", when_used="json", check_fields=False)
    def serialize_contract_values(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return format(value, "f")
        return value
