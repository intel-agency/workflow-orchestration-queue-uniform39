"""Abstract interfaces for the work queue (provider-agnostic).

All GitHub-specific logic is isolated behind these interfaces, enabling
future migration to other providers (Linear, Notion, SQL) without changing
the Sentinel's core dispatch logic (ADR-09).
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .models import WorkItem, WorkItemStatus


class ITaskQueue(ABC):
    """Provider-agnostic task queue interface.

    Implementations must be thread-safe and handle transient API errors internally.
    """

    @abstractmethod
    async def fetch_queued(self) -> list[WorkItem]:
        """Return all work items currently in the QUEUED state.

        Returns:
            List of WorkItem instances ready to be claimed.
        """

    @abstractmethod
    async def claim_task(self, item: WorkItem, sentinel_id: str) -> bool:
        """Attempt to claim exclusive ownership of a work item.

        Uses the provider's assignment mechanism as a distributed lock.
        Must be atomic from the provider's perspective.

        Args:
            item: The work item to claim.
            sentinel_id: Unique identifier of the claiming Sentinel instance.

        Returns:
            True if the claim succeeded; False if another Sentinel claimed it first.
        """

    @abstractmethod
    async def update_progress(self, item: WorkItem, log_line: str) -> None:
        """Post a progress update / heartbeat to the work item.

        Args:
            item: The work item being tracked.
            log_line: Sanitized log line to append to the item's audit trail.
        """

    @abstractmethod
    async def finish_task(
        self,
        item: WorkItem,
        status: WorkItemStatus,
        artifacts: dict[str, str] | None = None,
    ) -> None:
        """Mark a task as terminal (success or failure).

        Args:
            item: The work item to finalise.
            status: Terminal status to apply (SUCCESS, ERROR, INFRA_FAILURE, etc.).
            artifacts: Optional dict of artifact names to URLs (e.g. PR URL).
        """
