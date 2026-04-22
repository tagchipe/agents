"""Data models for Polymarket API responses."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Token:
    """Represents a token (outcome) in a Polymarket market."""

    token_id: str
    outcome: str
    price: float = 0.0
    winner: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Token":
        """Create a Token from a dictionary."""
        return cls(
            token_id=data.get("token_id", ""),
            outcome=data.get("outcome", ""),
            price=float(data.get("price", 0.0)),
            winner=data.get("winner", False),
        )


@dataclass
class Market:
    """Represents a Polymarket prediction market."""

    condition_id: str
    question_id: str
    question: str
    description: str
    market_slug: str
    end_date_iso: Optional[str]
    game_start_time: Optional[str]
    seconds_delay: int
    fpmm: str
    maker_base_fee: float
    taker_base_fee: float
    notifications_enabled: bool
    neg_risk: bool
    neg_risk_market_id: str
    neg_risk_request_id: str
    is_50_50_outcome: bool
    tokens: list[Token] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    active: bool = True
    closed: bool = False
    archived: bool = False
    accepting_orders: bool = True
    minimum_order_size: float = 5.0
    minimum_tick_size: float = 0.01
    volume: float = 0.0
    volume_24hr: float = 0.0
    liquidity: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> "Market":
        """Create a Market from a dictionary."""
        tokens = [
            Token.from_dict(t) for t in data.get("tokens", [])
        ]
        return cls(
            condition_id=data.get("condition_id", ""),
            question_id=data.get("question_id", ""),
            question=data.get("question", ""),
            description=data.get("description", ""),
            market_slug=data.get("market_slug", ""),
            end_date_iso=data.get("end_date_iso"),
            game_start_time=data.get("game_start_time"),
            seconds_delay=int(data.get("seconds_delay", 0)),
            fpmm=data.get("fpmm", ""),
            maker_base_fee=float(data.get("maker_base_fee", 0.0)),
            taker_base_fee=float(data.get("taker_base_fee", 0.0)),
            notifications_enabled=data.get("notifications_enabled", False),
            neg_risk=data.get("neg_risk", False),
            neg_risk_market_id=data.get("neg_risk_market_id", ""),
            neg_risk_request_id=data.get("neg_risk_request_id", ""),
            is_50_50_outcome=data.get("is_50_50_outcome", False),
            tokens=tokens,
            tags=data.get("tags", []),
            active=data.get("active", True),
            closed=data.get("closed", False),
            archived=data.get("archived", False),
            accepting_orders=data.get("accepting_orders", True),
            minimum_order_size=float(data.get("minimum_order_size", 5.0)),
            minimum_tick_size=float(data.get("minimum_tick_size", 0.01)),
            volume=float(data.get("volume", 0.0)),
            volume_24hr=float(data.get("volume_24hr", 0.0)),
            liquidity=float(data.get("liquidity", 0.0)),
        )

    def get_yes_token(self) -> Optional[Token]:
        """Return the YES outcome token if available."""
        for token in self.tokens:
            if token.outcome.upper() == "YES":
                return token
        return None

    def get_no_token(self) -> Optional[Token]:
        """Return the NO outcome token if available."""
        for token in self.tokens:
            if token.outcome.upper() == "NO":
                return token
        return None

    def is_tradeable(self) -> bool:
        """Check if the market is currently open for trading."""
        return self.active and not self.closed and not self.archived and self.accepting_orders
