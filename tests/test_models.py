"""Tests for Pydantic WorkItem models."""
from __future__ import annotations

from src.models import TaskType, WorkItem, WorkItemStatus


def test_work_item_defaults() -> None:
    item = WorkItem(
        id="123",
        source_url="https://github.com/org/repo/issues/123",
        context_body="Implement feature X",
        target_repo_slug="org/repo",
        task_type=TaskType.IMPLEMENT,
    )
    assert item.status == WorkItemStatus.QUEUED
    assert item.metadata == {}


def test_work_item_status_values() -> None:
    assert WorkItemStatus.QUEUED == "agent:queued"
    assert WorkItemStatus.IN_PROGRESS == "agent:in-progress"
    assert WorkItemStatus.SUCCESS == "agent:success"


def test_task_type_values() -> None:
    assert TaskType.PLAN == "plan"
    assert TaskType.IMPLEMENT == "implement"
    assert TaskType.REVIEW == "review"
    assert TaskType.BUGFIX == "bugfix"


def test_work_item_with_metadata() -> None:
    item = WorkItem(
        id="456",
        source_url="https://github.com/org/repo/issues/456",
        context_body="Fix bug Y",
        target_repo_slug="org/repo",
        task_type=TaskType.BUGFIX,
        status=WorkItemStatus.IN_PROGRESS,
        metadata={"issue_node_id": "I_abc123", "sentinel_id": "abc"},
    )
    assert item.metadata["sentinel_id"] == "abc"
    assert item.status == WorkItemStatus.IN_PROGRESS
