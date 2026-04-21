"""Polymarket API client for interacting with prediction markets.

Provides a unified interface to the Polymarket CLOB (Central Limit Order Book)
and Gamma (markets metadata) APIs.
"""

import os
from typing import Any, Optional

import requests
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_clob_client.constants import POLYGON

# Polymarket Gamma API base URL for market metadata
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

# Default timeout (seconds) for all outbound HTTP requests
DEFAULT_TIMEOUT = 30


class PolymarketClient:
    """Client for interacting with Polymarket APIs.

    Wraps both the CLOB client (for trading) and the Gamma API
    (for market discovery and metadata).
    """

    def __init__(
        self,
        private_key: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        api_passphrase: Optional[str] = None,
    ):
        """Initialize the Polymarket client.

        Args:
            private_key: Ethereum private key for signing transactions.
            api_key: Polymarket CLOB API key.
            api_secret: Polymarket CLOB API secret.
            api_passphrase: Polymarket CLOB API passphrase.
        """
        self.private_key = private_key or os.environ.get("PRIVATE_KEY", "")
        self.api_key = api_key or os.environ.get("POLYMARKET_API_KEY", "")
        self.api_secret = api_secret or os.environ.get("POLYMARKET_API_SECRET", "")
        self.api_passphrase = api_passphrase or os.environ.get(
            "POLYMARKET_API_PASSPHRASE", ""
        )

        self._clob_client: Optional[ClobClient] = None

    @property
    def clob(self) -> ClobClient:
        """Lazily initialize and return the CLOB client."""
        if self._clob_client is None:
            creds = ApiCreds(
                api_key=self.api_key,
                api_secret=self.api_secret,
                api_passphrase=self.api_passphrase,
            )
            self._clob_client = ClobClient(
                host=CLOB_API_BASE,
                chain_id=POLYGON,
                key=self.private_key,
                creds=creds,
            )
        return self._clob_client

    def get_markets(
        self,
        limit: int = 100,
        offset: int = 0,
        active: bool = True,
        closed: bool = False,
    ) -> list[dict[str, Any]]:
        """Fetch markets from the Gamma API.

        Args:
            limit: Maximum number of markets to return.
            offset: Pagination offset.
            active: If True, return only active markets.
            closed: If True, include closed markets.

        Returns:
            List of market objects.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "active": str(active).lower(),
            "closed": str(closed).lower(),
        }
        response = requests.get(
            f"{GAMMA_API_BASE}/markets", params=params, timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
