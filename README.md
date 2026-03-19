# workflow-orchestration-queue

> Headless agentic orchestration platform — turns GitHub Issues into autonomous AI execution orders.

## Overview

`workflow-orchestration-queue` transforms standard project management artifacts (GitHub Issues) into automated AI execution orders. A product manager writes an issue, applies a label, and walks away. The system dispatches an AI worker that clones the repo, generates code, runs tests, and submits a Pull Request — without human intervention.

**Architecture: 4 Pillars**

| Pillar | Component | Technology |
|--------|-----------|------------|
| The Ear | Webhook Notifier | FastAPI, Pydantic v2 |
| The State | Work Queue | GitHub Issues + Labels |
| The Brain | Sentinel Orchestrator | Python asyncio |
| The Hands | opencode Worker | opencode-server, DevContainer |

See [plan_docs/architecture.md](plan_docs/architecture.md) for full diagrams and [plan_docs/tech-stack.md](plan_docs/tech-stack.md) for the complete technology stack.

## Quickstart

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Docker + Docker Compose
- GitHub CLI (`gh`)
- `GITHUB_TOKEN` with `repo` and `project` scopes

### Setup

```bash
# Clone and enter the repo
git clone git@github.com:intel-agency/workflow-orchestration-queue-uniform39.git
cd workflow-orchestration-queue-uniform39

# Copy environment template
cp .env.example .env
# Edit .env and fill in GITHUB_TOKEN, ZHIPU_API_KEY, WEBHOOK_SECRET

# Install dependencies
uv sync

# Run tests
uv run pytest

# Start services locally
docker compose up
```

### Run Sentinel only

```bash
uv run sentinel
```

### Run Notifier only

```bash
uv run notifier
# Notifier listens on http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

## Development

```bash
# Install dev dependencies
uv sync --dev

# Lint
uv run ruff check src/ tests/

# Format
uv run black src/ tests/

# Type check
uv run mypy src/

# Run tests with coverage
uv run pytest
```

## Project Structure

```
src/
├── sentinel/
│   └── orchestrator_sentinel.py   # Polling background service
├── notifier/
│   └── notifier_service.py        # FastAPI webhook receiver
├── models.py                       # Shared Pydantic models (WorkItem, TaskType, etc.)
└── interfaces.py                   # ITaskQueue abstract base class
tests/
├── test_models.py
├── test_notifier.py
└── test_sentinel.py
plan_docs/                          # Project planning documents
docs/                               # Architecture decision records, API docs
scripts/                            # Shell bridge, auth utilities
.opencode/                          # AI agent definitions and commands
```

## GitHub Label State Machine

```
agent:queued → agent:in-progress → agent:success
                     ↓                   ↓
              agent:reconciling    (terminal)
                     ↓
         agent:error / agent:infra-failure / agent:impl-error
```

## Self-Bootstrapping

Once Phase 1 (Sentinel MVP) is deployed, the system manages its own evolution:

1. Open a GitHub Issue describing the next feature
2. Apply `agent:queued` label
3. The Sentinel picks it up and builds it

## Documentation

- [Application Plan](https://github.com/intel-agency/workflow-orchestration-queue-uniform39/issues/3)
- [Architecture Guide](plan_docs/architecture.md)
- [Development Plan](plan_docs/OS-APOW%20Development%20Plan%20v4.md)
- [Tech Stack](plan_docs/tech-stack.md)
- [AI Repository Summary](.ai-repository-summary.md)
- [Agent Instructions](AGENTS.md)

## License

MIT
