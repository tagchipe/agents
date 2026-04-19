"""Main entry point for the Polymarket trading agent."""

import os
import time
import logging
from dotenv import load_dotenv

from agents.application.trade import TradeAgent
from agents.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


def main():
    """Initialize and run the trading agent loop."""
    api_key = os.getenv("POLYMARKET_API_KEY")
    private_key = os.getenv("PRIVATE_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([api_key, private_key, openai_api_key]):
        logger.error(
            "Missing required environment variables. "
            "Please check your .env file against .env.example."
        )
        raise EnvironmentError("Required environment variables not set.")

    logger.info("Starting Polymarket trading agent...")

    agent = TradeAgent(
        api_key=api_key,
        private_key=private_key,
        openai_api_key=openai_api_key,
    )

    poll_interval = int(os.getenv("POLL_INTERVAL", "60"))

    while True:
        try:
            logger.info("Running agent cycle...")
            agent.run()
        except KeyboardInterrupt:
            logger.info("Agent stopped by user.")
            break
        except Exception as e:
            logger.exception("Unhandled error during agent cycle: %s", e)

        logger.info("Sleeping for %d seconds...", poll_interval)
        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
