# Agents

A fork of [Polymarket/agents](https://github.com/Polymarket/agents) — autonomous agents for prediction market trading on Polymarket.

## Overview

This project provides a framework for building and running AI-powered trading agents on Polymarket. Agents can autonomously research markets, reason about outcomes, and place trades.

## Features

- Autonomous market research and analysis
- LLM-powered reasoning for trade decisions
- Polymarket API integration
- Configurable agent strategies
- Docker support for deployment

## Requirements

- Python 3.11+
- Docker (optional)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/agents.git
cd agents
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```
POLYMARKET_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_key
PRIVATE_KEY=your_wallet_private_key
CHAIN_ID=137
```

> **Note:** I'm using `gpt-4o-mini` instead of `gpt-4o` to keep API costs low while experimenting.

### 4. Run an agent

```bash
python -m scripts.application
```

## Docker

Build and run with Docker:

```bash
docker build -t agents .
docker run --env-file .env agents
```

Or use the GitHub Actions workflow for automated builds.

## Project Structure

```
agents/
├── scripts/          # Entry points and CLI scripts
├── agents/           # Core agent logic
├── connectors/       # API connectors (Polymarket, LLMs)
├── utils/            # Shared utilities
└── tests/            # Test suite
```

## Notes (Personal)

- Running this in paper-trading / read-only mode for now — `POLYMARKET_API_KEY` left blank disables order placement.
- Useful reference for understanding the agent loop: `agents/agent.py` → `run()` method.
- Tested on Python 3.11.9; haven't tried 3.12 yet.
- The agent loop runs every 60s by default — bumped mine to 120s to reduce API calls during testing.
- Noticed the agent sometimes errors silently when a market has no open orders; added a `try/except` around the order fetch in my local copy (`connectors/clob.py` ~line 84).
- Logging was pretty sparse, so I added a basic file handler in `utils/logger.py` to write logs to `agent.log` — handy for reviewing what happened after a run.
- Set `MAX_MARKETS` to 5 (down from 20) so each run stays focused and finishes faster during testing — too many markets at once made the LLM calls expensive.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Open a pull request

Please use the issue templates for bug reports and feature requests.

## License

MIT
