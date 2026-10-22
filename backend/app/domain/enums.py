"""Stable enum values shared by API contracts and persistence models."""

from enum import StrEnum


class AccountType(StrEnum):
    OPERATING = "operating"
    TREASURY_RESERVE = "treasury_reserve"
    RESTRICTED = "restricted"


class ObligationType(StrEnum):
    PAYROLL = "payroll"
    TAX = "tax"
    ACCOUNTS_PAYABLE = "accounts_payable"
    CARD_SETTLEMENT = "card_settlement"
    DEBT = "debt"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class TransactionStatus(StrEnum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationAction(StrEnum):
    ALLOCATE = "allocate"
    HOLD = "hold"
    PULL_BACK = "pull_back"
    REVIEW_REQUIRED = "review_required"


class Freshness(StrEnum):
    FRESH = "fresh"
    WARNING = "warning"
    STALE = "stale"
    ERROR = "error"


class ObligationCertainty(StrEnum):
    CONFIRMED = "confirmed"
    EXPECTED = "expected"
    UNCERTAIN = "uncertain"


class BufferStrategy(StrEnum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    MAXIMUM = "maximum"


class RecommendationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    SUPERSEDED = "superseded"


class DecisionAction(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    DEFER = "defer"
    OVERRIDE = "override"
