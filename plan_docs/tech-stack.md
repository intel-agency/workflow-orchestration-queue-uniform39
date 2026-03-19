# Technology Stack: workflow-orchestration-queue

## Primary Language

- **Python 3.12+** — Main language for all orchestration logic and API services
  - Leverages `asyncio` for concurrent background polling and event handling
  - Type annotations throughout for maintainability and tooling support

## Secondary Languages / Shell

- **PowerShell Core (pwsh)** — Auth scripts, label import, repo setup utilities
- **Bash** — Devcontainer lifecycle hooks, shell-bridge scripts

## Package Management

- **uv** — Ultra-fast Python package resolver and installer (replaces pip/venv)
  - All dependency management via `pyproject.toml` + `uv.lock`
  - Run commands: `uv sync`, `uv run <cmd>`

## Frameworks

| Layer | Framework/Library | Version | Purpose |
|---|---|---|---|
| API / Webhook | **FastAPI** | ^0.115 | HTTP webhook receiver ("The Ear") |
| Data Validation | **Pydantic v2** | ^2.9 | Schema validation, WorkItem models |
| Async Runtime | **asyncio** (stdlib) | 3.12 built-in | Sentinel background polling loop |
| HTTP Client | **httpx** | ^0.27 | GitHub API calls from Python |
| Auth | **PyJWT** | ^2.9 | GitHub App JWT token generation |
| ASGI Server | **uvicorn** | ^0.31 | FastAPI production server |

## AI Worker Runtime

- **opencode CLI / opencode-server** — LLM agent execution shell
- **GLM-5** (ZhipuAI `zai-coding-plan/glm-5`) — Default model via `ZHIPU_API_KEY`
- **Claude 3.5 Sonnet** — Alternate high-stakes model

## Testing

- **pytest** — Test runner
- **pytest-asyncio** — Async test support
- **pytest-cov** — Coverage reporting
- **httpx** — HTTP integration testing (TestClient for FastAPI)
- Coverage target: **80%+**

## Linting & Formatting

- **ruff** — Fast linter (replaces flake8, isort, pyupgrade)
- **black** — Code formatter
- **mypy** — Static type checking

## Containerisation

- **Docker** — Container runtime for Worker DevContainers
- **Docker Compose** — Multi-container orchestration (Sentinel + Notifier + dependencies)
- `devcontainer.json` — VS Code / GitHub Codespaces devcontainer spec

## Infrastructure / CI-CD

- **GitHub Actions** — CI/CD pipelines (validate, publish-docker, prebuild-devcontainer)
- **GHCR** — GitHub Container Registry for Docker image storage
- **GitHub Projects v2** — Issue tracking / Kanban board

## GitHub Integration

- **GitHub REST API** — Issue/label/milestone/project management
- **GitHub App (HMAC SHA-256)** — Webhook signature verification
- **gh CLI** — Local admin tooling (milestones, labels, PR management)

## Key Environment Variables

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` / `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub API auth |
| `ZHIPU_API_KEY` | ZhipuAI GLM model access |
| `WEBHOOK_SECRET` | HMAC secret for verifying GitHub webhook payloads |
| `SENTINEL_ID` | Unique identifier for each Sentinel instance |
| `TASK_TIMEOUT_MINUTES` | Max time before a task is considered stale (default: 120) |
| `DAILY_BUDGET_TOKENS` | Daily LLM token budget guardrail |
