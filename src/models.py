"""Pydantic models for workflow-orchestration-queue.

Defines the core data structures shared across the Sentinel and Notifier components.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    """Classification of work item intent."""

    PLAN = "plan"
    IMPLEMENT = "implement"
    REVIEW = "review"
    BUGFIX = "bugfix"


class WorkItemStatus(StrEnum):
    """Mirrors the GitHub label state machine for agent task status."""

    QUEUED = "agent:queued"
    IN_PROGRESS = "agent:in-progress"
    RECONCILING = "agent:reconciling"
    SUCCESS = "agent:success"
    ERROR = "agent:error"
    INFRA_FAILURE = "agent:infra-failure"
    IMPL_ERROR = "agent:impl-error"
    STALLED_BUDGET = "agent:stalled-budget"


class WorkItem(BaseModel):
    """Unified representation of a unit of work, provider-agnostic.

    Created by the Notifier on webhook ingestion, or by the Sentinel when
    polling GitHub Issues. Passed to the Worker via the shell-bridge prompt.
    """

    id: str = Field(description="Provider-specific issue identifier (e.g. GitHub issue number)")
    source_url: str = Field(description="URL of the originating issue or event")
    context_body: str = Field(description="Full markdown body of the issue (sanitized)")
    target_repo_slug: str = Field(
        description="owner/repo that the agent should operate against"
    )
    task_type: TaskType = Field(description="Classification of the work item")
    status: WorkItemStatus = Field(default=WorkItemStatus.QUEUED)
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific extras (e.g. issue_node_id, pr_number, reviewer_comments)",
    )
