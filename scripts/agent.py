"""Main entry point for the Polymarket trading agent."""

import os
import time
import logging
from dotenv import load_dotenv

from agents.application.trade import TradeAgent
from agents.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

# Default poll interval increased to 5 minutes to avoid hammering the API
DEFAULT_POLL_INTERVAL = "300"

# Maximum number of consecutive errors before giving up
# Reduced from 5 to 3 - I'd rather have the agent stop sooner and alert me
# than silently retry many times with a broken state
MAX_CONSECUTIVE_ERRORS = 3

# How long to wait (seconds) before retrying after an error, instead of
# immediately sleeping the full poll interval. Helps recover faster.
# Bumped from 30 to 60 - 30s felt too aggressive when the API is having issues
ERROR_RETRY_DELAY = 60

# Back off multiplier: each consecutive error waits a bit longer before retry.
# e.g. 1st error: 60s, 2nd error: 120s. Avoids hammering a struggling API.
ERROR_RETRY_BACKOFF = 2


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

    poll_interval = int(os.getenv("POLL_INTERVAL", DEFAULT_POLL_INTERVAL))
    consecutive_errors = 0

    while True:
        try:
            logger.info("Running agent cycle...")
            agent.run()
            consecutive_errors = 0
        except KeyboardInterrupt:
            logger.info("Agent stopped by user.")
            break
        except Exception as e:
            logger.exception("Unhandled error during agent cycle: %s", e)
            consecutive_errors += 1
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                logger.error(
                    "Reached %d consecutive errors, stopping agent.",
                    MAX_CONSECUTIVE_ERRORS,
                )
                break
            # Apply exponential backoff so repeated failures wait progressively longer
            retry_delay = ERROR_RETRY_DELAY * (ERROR_RETRY_BACKOFF ** (consecutive_errors - 1))
            logger.info("Error encountered, retrying in %d seconds...", retry_delay)
            time.sleep(retry_delay)
            continue

        logger.info("Sleeping for %d seconds...", poll_interval)
        time.sleep(poll_interval)


if __name__ == "__main__":
    main()
