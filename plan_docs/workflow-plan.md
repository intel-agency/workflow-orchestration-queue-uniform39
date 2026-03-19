# Workflow Execution Plan: project-setup

**Workflow File:** [`ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md`](https://github.com/nam20485/agent-instructions/blob/main/ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md)  
**Generated:** 2026-03-19  
**Branch:** `dynamic-workflow-project-setup`  
**Status:** Ready for Stakeholder Approval

---

## 1. Overview

- **Workflow Name:** `project-setup`
- **Project Name:** `workflow-orchestration-queue` (also referred to as OS-APOW)
- **Repository:** `intel-agency/workflow-orchestration-queue-uniform39`
- **Total Assignments:** 6 primary + 1 pre-script event + 2 post-assignment events
- **Summary:** This workflow initialises the freshly-seeded template repository for the `workflow-orchestration-queue` project — a headless agentic orchestration platform written in Python 3.12. It creates the GitHub project board, imports labels, creates a working branch, produces a detailed application plan (as a GitHub Issue), scaffolds the project file structure, creates repository summary and AGENTS.md documentation, and closes with a debrief.

---

## 2. Project Context Summary

| Fact | Value |
|---|---|
| **Repository** | `intel-agency/workflow-orchestration-queue-uniform39` |
| **Primary Language** | Python 3.12+ |
| **Secondary Languages** | PowerShell Core (pwsh), Bash |
| **Package Manager** | `uv` (ultra-fast pip replacement) |
| **Frameworks** | FastAPI (Ear/webhook receiver), asyncio (Sentinel background service), Pydantic v2 (schema validation) |
| **Containerisation** | Docker + Docker Compose, GitHub devcontainers |
| **AI Worker Runtime** | opencode CLI / opencode-server, GLM-5 / Claude 3.5 Sonnet |
| **Infrastructure** | GitHub Actions, GHCR, devcontainer prebuild pipeline |
| **Key Plan Docs** | `OS-APOW Implementation Specification v1.md`, `OS-APOW Development Plan v4.md`, `OS-APOW Architecture Guide v3.md` |
| **Skeleton Files** | `plan_docs/notifier_service.py`, `plan_docs/orchestrator_sentinel.py` |
| **Current Branch** | `main` (HEAD ahead of origin by 1 commit) |
| **Special Constraints** | No `.NET` application structure needed — this is a **Python** project. `global.json` and `.NET SDK 10` devcontainer tools are part of the template scaffolding and unrelated to the application code itself. |
| **Phase Roadmap** | Phase 0: Seeding & Bootstrapping (current) → Phase 1: Sentinel MVP → Phase 2: Ear/Webhook → Phase 3: Deep Orchestration |

**Key architectural decisions influencing this workflow:**
- "Script-First Integration": All worker interactions use `./scripts/devcontainer-opencode.sh` shell bridge.
- "Markdown as a Database": GitHub Issues + Labels are the state machine.
- "Self-Bootstrapping": The platform is designed to build itself using its own orchestration capabilities after Phase 1 is live.

---

## 3. Assignment Execution Plan

### Pre-Script Event: `create-workflow-plan`

| Field | Content |
|---|---|
| **Assignment** | `create-workflow-plan`: Create Workflow Plan |
| **Goal** | Produce a comprehensive, project-specific workflow execution plan and get stakeholder approval before any other assignment begins |
| **Key Acceptance Criteria** | Dynamic workflow fully read; all assignments traced; all `plan_docs/` read; plan documented as `plan_docs/workflow-plan.md`; stakeholder-approved; committed and pushed |
| **Project-Specific Notes** | Plan docs include three major planning documents plus two Python skeleton files (`notifier_service.py`, `orchestrator_sentinel.py`). The implementation will be Python 3.12 + FastAPI + async, not .NET. |
| **Prerequisites** | None — this is the first step |
| **Dependencies** | None |
| **Risks / Challenges** | Template repo AGENTS.md references template placeholder names (`workflow-orchestration-queue-uniform39`, `intel-agency`) that may need updating in `create-agents-md-file`. |
| **Events** | None |

---

### Assignment 1: `init-existing-repository`

| Field | Content |
|---|---|
| **Assignment** | `init-existing-repository`: Initiate Existing Repository |
| **Goal** | Create GitHub Project board, import labels, rename workspace/devcontainer files to match repo name, create working branch `dynamic-workflow-project-setup` |
| **Key Acceptance Criteria** | GitHub Project created (Board view, correct columns); project linked to repo; labels imported from `.github/.labels.json`; `devcontainer.json` `name` field updated; `.code-workspace` file renamed if needed; PR/branch created |
| **Project-Specific Notes** | The `.devcontainer/devcontainer.json` already has `name: "workflow-orchestration-queue-uniform39-build"` — it should be renamed to `workflow-orchestration-queue-uniform39-devcontainer` per the template. The `.code-workspace` file is already named `workflow-orchestration-queue-uniform39.code-workspace` (correct). Labels file is at `.github/.labels.json`. |
| **Prerequisites** | GitHub CLI (`gh`) authenticated with `repo`, `project`, `read:project`, `read:user`, `user:email` scopes. Run `./scripts/test-github-permissions.ps1` to verify. |
| **Dependencies** | None — first content assignment |
| **Risks / Challenges** | GitHub Project scope requires `project` + `read:project` OAuth scopes on the token. The `import-labels.ps1` script requires `pwsh` (PowerShell Core). If permissions are missing, use `./scripts/gh-auth.ps1` to re-authenticate. |
| **Events** | Post: `validate-assignment-completion`, `report-progress` |

---

### Assignment 2: `create-app-plan`

| Field | Content |
|---|---|
| **Assignment** | `create-app-plan`: Create Application Plan |
| **Goal** | Produce a detailed phased application plan as a GitHub Issue using the `.github/ISSUE_TEMPLATE/application-plan.md` template; create milestones; link to GitHub Project; apply labels |
| **Key Acceptance Criteria** | All plan docs analysed; tech-stack.md created in `plan_docs/`; architecture.md created in `plan_docs/`; issue created using template with all sections completed; milestones created (at minimum one per phase); issue assigned to Phase 1 milestone; labels `planning`, `documentation`, and `implementation:ready` applied |
| **Project-Specific Notes** | The primary spec is `plan_docs/OS-APOW Implementation Specification v1.md`. Tech stack: Python 3.12, FastAPI, uv, asyncio, Pydantic, Docker, GitHub API. Architecture is event-driven with 4 pillars: Ear, State (Queue), Brain (Sentinel), Hands (Worker). All four phases must be documented as plan phases/milestones: Phase 0 (Seeding), Phase 1 (Sentinel MVP), Phase 2 (Ear), Phase 3 (Deep Orchestration). |
| **Prerequisites** | `init-existing-repository` completed; branch `dynamic-workflow-project-setup` exists |
| **Dependencies** | Output from `#initiate-new-repository.init-existing-repository` (project board, labels, branch) |
| **Risks / Challenges** | **Planning only — no code to be written.** The existing `plan_docs/notifier_service.py` and `plan_docs/orchestrator_sentinel.py` are reference skeletons from human-authored planning, not from a prior assignment — treat them as planning context, not implementation artifacts. |
| **Events** | Pre: `gather-context`; Post: `validate-assignment-completion`, `report-progress`, `report-progress`; On failure: `recover-from-error` |

---

### Assignment 3: `create-project-structure`

| Field | Content |
|---|---|
| **Assignment** | `create-project-structure`: Create Project Structure |
| **Goal** | Create the actual Python project scaffolding — directory layout, configuration files, Dockerfiles, CI/CD workflows foundation, README.md, and initial test structure |
| **Key Acceptance Criteria** | Python project structure created following the plan; `pyproject.toml` or `uv`-compatible project config created; Dockerfile(s) created for each service; docker-compose.yml created; configuration/env templates created; README.md created; docs/ directory structure created; `.github/workflows/` structure established; initial `uv` environment validates; project structure reviewed and approved by stakeholder; `.ai-repository-summary.md` created (see assignment 4) |
| **Project-Specific Notes** | This is a **Python** project, not .NET. Project structure should follow Python/uv conventions: `src/` layout with `sentinel/` and `notifier/` sub-packages (or a monorepo structure). Key files: `pyproject.toml`, `uv.lock`, `src/sentinel/orchestrator_sentinel.py`, `src/notifier/notifier_service.py`, `src/models.py`, `src/interfaces.py`, `tests/`, `Dockerfile.sentinel`, `Dockerfile.notifier`, `docker-compose.yml`. Reference skeleton files in `plan_docs/` for initial structure hints. The existing `global.json` and `.NET SDK 10` settings in the devcontainer are for the orchestration framework (opencode), not the application — do not remove them. |
| **Prerequisites** | `create-app-plan` completed; approved application plan issue exists with milestones |
| **Dependencies** | `#initiate-new-repository.create-app-plan` (application plan, tech-stack.md, architecture.md, milestones) |
| **Risks / Challenges** | `uv` must be installed in the devcontainer (it is, per `.github/.devcontainer/Dockerfile`). The project structure should not conflict with the template framework files (`.opencode/`, `.github/workflows` orchestration workflows, devcontainer configs). New Python project files go in the repo root or a `src/` subdirectory. |
| **Events** | Post: `validate-assignment-completion`, `report-progress` |

---

### Assignment 4: `create-repository-summary`

| Field | Content |
|---|---|
| **Assignment** | `create-repository-summary`: Create Repository Summary |
| **Goal** | Create `.ai-repository-summary.md` at the repository root — a concise, agent-optimised document covering project purpose, tech stack, build/test commands, project layout, CI/CD details, and coding conventions |
| **Key Acceptance Criteria** | `.ai-repository-summary.md` created at repo root; covers project overview, tech stack, verified build/test commands, project layout, CI/CD pipeline steps, coding conventions; file under 32K tokens; committed and pushed to working branch; stakeholder approval obtained |
| **Project-Specific Notes** | Build commands to document: `uv sync`, `uv run pytest`, `uv run python -m sentinel`, `docker compose up`. Linting: `uv run ruff check`, `uv run black --check`. Key paths: `src/sentinel/`, `src/notifier/`, `src/models.py`, `src/interfaces.py`, `tests/`. CI/CD: `.github/workflows/validate.yml` (lint, scan, test), `publish-docker.yml`, `prebuild-devcontainer.yml`. Note that `opencode serve` starts on port 4096 via devcontainer lifecycle. |
| **Prerequisites** | `create-project-structure` completed; verified build commands available |
| **Dependencies** | `#initiate-new-repository.create-project-structure` (confirmed project structure, validated build commands) |
| **Risks / Challenges** | Build commands must be validated by actually running them in the devcontainer before documenting. Commands that require network access (GitHub API tokens) should be documented with expected env vars. |
| **Events** | Post: `validate-assignment-completion`, `report-progress` |

---

### Assignment 5: `create-agents-md-file`

| Field | Content |
|---|---|
| **Assignment** | `create-agents-md-file`: Create AGENTS.md File |
| **Goal** | Create (or update) `AGENTS.md` at the repository root with project-specific, agent-optimised instructions covering setup, build, test, code style, project structure, testing, and PR/commit guidelines |
| **Key Acceptance Criteria** | `AGENTS.md` exists at repo root; contains project overview, setup commands, project structure, code style, testing instructions, PR/commit guidelines; all listed commands have been validated; file committed and pushed; stakeholder approval obtained |
| **Project-Specific Notes** | The existing `AGENTS.md` at repo root is the **template-level** AGENTS.md covering the orchestration framework, not the application. It must be updated to reflect the `workflow-orchestration-queue` application layer: Python 3.12, FastAPI, uv, ruff, black, pytest. Preserve the existing orchestration framework context in a clearly separated section. Key update: replace/augment the template's `<tech_stack>` and `<repository_map>` with project-specific Python entries. |
| **Prerequisites** | `create-project-structure` completed; `create-repository-summary` completed; validated build and test commands available |
| **Dependencies** | `#initiate-new-repository.create-repository-summary` (validated commands, `.ai-repository-summary.md`) |
| **Risks / Challenges** | The existing `AGENTS.md` is XML-structured template content. Carefully decide whether to update the existing file (preferred) or replace it. Must not destroy the orchestration framework instructions used by the opencode agents. |
| **Events** | Post: `validate-assignment-completion`, `report-progress` |

---

### Assignment 6: `debrief-and-document`

| Field | Content |
|---|---|
| **Assignment** | `debrief-and-document`: Debrief and Document Learnings |
| **Goal** | Produce a comprehensive 12-section debrief report of the project-setup workflow run, commit it, and initiate continuous improvement |
| **Key Acceptance Criteria** | All 12 report sections completed; execution trace saved as `debrief-and-document/trace.md`; report reviewed and approved by stakeholder; report committed and pushed; `continuous-improvement` assignment delegated |
| **Project-Specific Notes** | Debrief should specifically call out: the Python-vs-.NET tech stack distinction (template default vs project reality), any GitHub Project permission issues encountered, any `uv`/Python environment setup challenges, the state of the devcontainer prebuild pipeline (images may not yet exist on first clone). |
| **Prerequisites** | All prior assignments completed and approved |
| **Dependencies** | All `#initiate-new-repository.*` outputs |
| **Risks / Challenges** | This is the final assignment — ensure all prior work is committed before beginning the debrief. If any prior assignment is still in progress, complete it first. |
| **Events** | Post: `validate-assignment-completion`, `report-progress` |

---

## 4. Post-Assignment Events (Fire After Every Assignment)

After each primary assignment completes, two event assignments fire in sequence:

### Event: `validate-assignment-completion`

- Checks all expected file outputs exist
- Runs appropriate verification commands (for Python: `uv sync`, `uv run ruff check`, `uv run pytest`)
- Creates validation report at `docs/validation/VALIDATION_REPORT_<assignment-name>_<timestamp>.md`
- Determines PASS/FAIL; halts workflow on FAIL
- **Must be executed by an independent `qa-test-engineer` agent** (not the agent that performed the assignment)

### Event: `report-progress`

- Generates structured progress update (step name, duration, status, outputs, overall progress, next step)
- Records outputs with step-tagged references for downstream assignments
- Saves workflow checkpoint state for resume capability
- Posts progress notification to user

---

## 5. Sequencing Diagram

```
pre-script-begin
  └── create-workflow-plan ✅ (this document)
        │
        ▼
script: initiate-new-repository
  ┌──────────────────────────────────────────────────┐
  │  1. init-existing-repository                     │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  │                                                  │
  │  2. create-app-plan                              │
  │     └── pre: gather-context                      │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  │     └── on-failure: recover-from-error           │
  │                                                  │
  │  3. create-project-structure                     │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  │                                                  │
  │  4. create-repository-summary                    │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  │                                                  │
  │  5. create-agents-md-file                        │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  │                                                  │
  │  6. debrief-and-document                         │
  │     └── post: validate-assignment-completion     │
  │     └── post: report-progress                    │
  └──────────────────────────────────────────────────┘
```

---

## 6. Open Questions

1. **GitHub Project visibility:** Should the GitHub Project be public or private? (Default: private, matching repository visibility)
2. **Python project layout:** Should the project use a flat `src/` layout or separate top-level packages (`sentinel/`, `notifier/`)? The skeleton files in `plan_docs/` suggest a flat structure — confirm preference.
3. **AGENTS.md update strategy:** Should the existing template-level AGENTS.md be replaced entirely with project-specific content, or should it be updated to include both the framework context AND the application context in separate sections? Recommendation: update with clear sections.
4. **Branch strategy for PRs:** The `init-existing-repository` assignment creates branch `dynamic-workflow-project-setup` from `main`. Should this be a long-running feature branch (all assignments commit here, one final PR to `main`) or should each assignment have its own PR? Recommendation: single branch, single PR at end.
5. **Devcontainer image availability:** The consumer devcontainer (`/.devcontainer/devcontainer.json`) references a prebuilt GHCR image that does not yet exist (first clone from template). The `create-project-structure` validation step may need to fall back to local Dockerfile build. This is expected per the template design constraints.

---

*This plan was produced by the `create-workflow-plan` pre-script event of the `project-setup` dynamic workflow.*  
*Reference: [project-setup.md](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md)*
