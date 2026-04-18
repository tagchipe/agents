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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Open a pull request

Please use the issue templates for bug reports and feature requests.

## License

MIT
