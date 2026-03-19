# Architecture: workflow-orchestration-queue

## Overview

`workflow-orchestration-queue` is a **headless agentic orchestration platform** built on an event-driven, strictly decoupled architecture. It transforms standard GitHub Issues into autonomous AI execution orders, replacing human-in-the-loop coding workflows with a persistent background production service.

The architecture follows a **4-Pillar model**, each with a clear domain boundary:

```
┌─────────────────────────────────────────────────────────────┐
│              workflow-orchestration-queue                    │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  The Ear    │    │  The State   │    │  The Brain    │  │
│  │  (Notifier) │───▶│  (Queue)     │───▶│  (Sentinel)   │  │
│  │  FastAPI    │    │  GitHub      │    │  Python async │  │
│  │  Webhooks   │    │  Issues +    │    │  background   │  │
│  │  HMAC auth  │    │  Labels      │    │  polling svc  │  │
│  └─────────────┘    └──────────────┘    └───────┬───────┘  │
│                                                  │          │
│                                          devcontainer-      │
│                                          opencode.sh        │
│                                                  │          │
│                                         ┌────────▼───────┐  │
│                                         │  The Hands     │  │
│                                         │  (Worker)      │  │
│                                         │  opencode-     │  │
│                                         │  server        │  │
│                                         │  DevContainer  │  │
│                                         └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Pillar 1: The Ear (Work Event Notifier)

**File:** `src/notifier/notifier_service.py`  
**Technology:** Python 3.12, FastAPI, uvicorn, Pydantic v2  
**Port:** 8000 (configurable)

### Responsibilities
- Expose `/webhooks/github` POST endpoint
- Validate `X-Hub-Signature-256` HMAC SHA-256 header on every request
- Reject any request with invalid/missing signature with HTTP 401 (before JSON parsing)
- Parse GitHub event payloads into `WorkItem` Pydantic models
- Apply `agent:queued` label via GitHub REST API to trigger the Sentinel
- Return HTTP 202 Accepted within 10 seconds (GitHub webhook timeout)
- Expose Swagger/OpenAPI docs at `/docs`

### Security
- HMAC verification using `WEBHOOK_SECRET` env var
- Protects against "Prompt Injection via Webhook" — only verified GitHub App events are processed
- No payload processing before signature validation

---

## Pillar 2: The State (Work Queue)

**Technology:** GitHub Issues, Labels, Milestones (Markdown as a Database)

### State Machine

```
agent:queued ──▶ agent:in-progress ──▶ agent:success
                     │                      │
                     ▼                      ▼
              agent:reconciling       (terminal)
                     │
                     ▼ (stale/crash)
               re-queue or
               agent:error / agent:infra-failure / agent:stalled-budget
```

### Label Semantics

| Label | Meaning |
|---|---|
| `agent:queued` | Task validated; awaiting Sentinel claim |
| `agent:in-progress` | Sentinel claimed task; worker executing |
| `agent:reconciling` | Stale in-progress task under re-evaluation |
| `agent:success` | Worker completed; PR submitted |
| `agent:error` | Technical failure; last 50 lines of stderr posted as comment |
| `agent:infra-failure` | Container startup failure |
| `agent:impl-error` | Agent logic/prompt failure |
| `agent:stalled-budget` | Daily token budget exceeded |

### Concurrency Control
- GitHub Assignees used as distributed lock semaphore
- Sentinel must successfully assign issue to itself before transitioning to `agent:in-progress`
- Prevents race conditions in multi-Sentinel deployments

---

## Pillar 3: The Brain (Sentinel Orchestrator)

**File:** `src/sentinel/orchestrator_sentinel.py`  
**Technology:** Python 3.12, asyncio, httpx, GitHub REST API

### Responsibilities
- Poll GitHub every 60 seconds for issues labelled `agent:queued`
- Run `scripts/gh-auth.ps1` + `scripts/common-auth.ps1` to sync credentials before dispatch
- Claim tasks via GitHub Assignee API (distributed lock)
- Manage worker lifecycle via `./scripts/devcontainer-opencode.sh` shell bridge:
  - `up` — provision Docker network and volumes
  - `start` — launch opencode-server inside devcontainer
  - `prompt "{instruction}"` — dispatch task to worker
- Map issue type/label to correct workflow instruction module
- Stream worker stdout to local JSONL log files
- Post periodic heartbeat comments to GitHub Issues
- Handle exit codes: 0=success, 1–10=infra error, 11+=logic error
- Implement jittered exponential backoff for GitHub API rate limit errors
- Monitor daily LLM budget; halt and label `agent:stalled-budget` if exceeded
- Run reconciliation loop: detect stale `agent:in-progress` tasks (>TASK_TIMEOUT_MINUTES) and re-queue

### Unique Instance Identification
- Each Sentinel generates or accepts a `SENTINEL_ID` on startup
- All issue actions attributed to the Sentinel identity

---

## Pillar 4: The Hands (Opencode Worker)

**Technology:** opencode-server CLI, GLM-5 / Claude 3.5 Sonnet, DevContainer  
**Entry:** `./scripts/devcontainer-opencode.sh`

### Responsibilities
- Run inside isolated Docker DevContainer derived from this repository's image
- Execute markdown-based workflow instruction modules from `/local_ai_instruction_modules/`
- Clone/pull target repository into managed workspace volume
- Run `./scripts/update-remote-indices.ps1` for vector-indexed codebase access
- Generate code, run tests within container, submit PR
- Pipe output through credential scrubber before posting to GitHub

### Security
- Runs in segrated bridge Docker network (no host subnet access)
- Cgroup limits: 2 CPUs, 4GB RAM
- GitHub Installation Token injected as ephemeral env var; destroyed on container exit
- All output scrubbed via regex before posting to GitHub

---

## Key Architectural Decisions

### ADR-07: Script-First Shell Bridge
All worker interactions via `./scripts/devcontainer-opencode.sh` only — no direct Docker SDK. Ensures environment parity between AI runs and human developer runs.

### ADR-08: Polling-First Resiliency
Polling is primary; webhooks are optional optimisation. Guarantees self-healing on restart. Sentinel always reconciles state from GitHub labels, never from local memory alone.

### ADR-09: Provider-Agnostic Interface
All queue interactions behind `ITaskQueue` interface:
- `fetch_queued()` — return list of WorkItem
- `claim_task(id, sentinel_id)` — acquire lock
- `update_progress(id, log_line)` — heartbeat
- `finish_task(id, artifacts)` — terminal state

Allows future migration to Linear, Notion, or SQL queues without changing orchestrator core logic.

---

## Repository Directory Structure (Target)

```
workflow-orchestration-queue-uniform39/
├── src/
│   ├── sentinel/
│   │   ├── __init__.py
│   │   └── orchestrator_sentinel.py   # Sentinel polling service
│   ├── notifier/
│   │   ├── __init__.py
│   │   └── notifier_service.py        # FastAPI webhook receiver
│   ├── models.py                       # WorkItem, WorkItemType, WorkItemStatus Pydantic models
│   └── interfaces.py                   # ITaskQueue abstract base class
├── tests/
│   ├── test_notifier.py
│   ├── test_sentinel.py
│   └── test_models.py
├── plan_docs/                          # Planning documents (seeded from template)
├── docs/                               # Architecture, API docs, ADRs
├── scripts/                            # Shell bridge, auth, admin utilities
├── .opencode/agents/                   # AI agent definitions
├── .opencode/commands/                 # opencode command prompts
├── .github/workflows/                  # CI/CD pipelines
├── .devcontainer/devcontainer.json     # Consumer devcontainer
├── Dockerfile.sentinel                 # Sentinel service container
├── Dockerfile.notifier                 # Notifier service container
├── docker-compose.yml                  # Local dev multi-service orchestration
├── pyproject.toml                      # Python project config + uv dependencies
├── uv.lock                             # Locked dependency manifest
├── AGENTS.md                           # AI agent instructions
└── README.md
```

---

## Data Flow (Happy Path)

1. User opens GitHub Issue with `[Application Plan]` prefix
2. GitHub Webhook fires → **Notifier** validates HMAC signature
3. Notifier parses payload into `WorkItem`; applies `agent:queued` label
4. **Sentinel** polling cycle detects new label; assigns issue to itself
5. Sentinel transitions label to `agent:in-progress`; clones/pulls target repo
6. Sentinel runs `devcontainer-opencode.sh up`
7. Sentinel dispatches: `devcontainer-opencode.sh prompt "<workflow instruction>"`
8. **Worker** runs inside DevContainer; generates code; runs tests; creates PR
9. Worker posts execution complete comment; exits 0
10. Sentinel detects exit code; removes `agent:in-progress`; applies `agent:success`
