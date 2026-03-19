"""Sentinel Orchestrator — persistent background polling service.

Polls GitHub for queued work items, claims them, dispatches to the opencode
Worker via the devcontainer shell bridge, and reports status back to GitHub.

Architecture: see plan_docs/architecture.md — Pillar 3: The Brain.

Usage:
    uv run python -m sentinel.orchestrator_sentinel
    # or via project script:
    uv run sentinel
"""
from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import sys
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants / configuration (overridable via environment variables)
# ---------------------------------------------------------------------------

POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
TASK_TIMEOUT_MINUTES: int = int(os.getenv("TASK_TIMEOUT_MINUTES", "120"))
HEARTBEAT_INTERVAL_MINUTES: int = int(os.getenv("HEARTBEAT_INTERVAL_MINUTES", "5"))
SHELL_BRIDGE_SCRIPT: str = os.getenv(
    "SHELL_BRIDGE_SCRIPT", "./scripts/devcontainer-opencode.sh"
)

# Exit code ranges for the shell bridge (ADR-07)
INFRA_ERROR_RANGE: range = range(1, 11)   # 1–10: container/infra failure
LOGIC_ERROR_RANGE: range = range(11, 256)  # 11+:  agent/logic failure


class SentinelOrchestrator:
    """Core polling and dispatch engine.

    Responsibilities:
    - Discover queued work items via ITaskQueue.fetch_queued()
    - Claim items using GitHub Assignees as distributed lock
    - Dispatch to worker via shell-bridge
    - Post progress heartbeats
    - Report terminal status (success / infra-failure / impl-error)
    - Enforce daily budget guardrails
    - Reconcile stale in-progress tasks
    """

    def __init__(self, sentinel_id: str | None = None) -> None:
        self.sentinel_id: str = sentinel_id or str(uuid.uuid4())[:8]
        self._running: bool = False
        logger.info("Sentinel %s initialised", self.sentinel_id)

    async def run(self) -> None:
        """Start the main polling loop. Runs until stopped."""
        self._running = True
        logger.info(
            "Sentinel %s starting poll loop (interval=%ds)",
            self.sentinel_id,
            POLL_INTERVAL_SECONDS,
        )
        while self._running:
            try:
                await self._poll_cycle()
            except Exception:
                logger.exception("Unhandled error in poll cycle")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)

    def stop(self) -> None:
        """Signal the polling loop to stop after the current cycle."""
        self._running = False
        logger.info("Sentinel %s stopping", self.sentinel_id)

    async def _poll_cycle(self) -> None:
        """Single poll iteration: discover, claim, and dispatch queued items."""
        # TODO (Phase 1): inject ITaskQueue implementation
        # queued = await self.queue.fetch_queued()
        # for item in queued:
        #     if await self.queue.claim_task(item, self.sentinel_id):
        #         asyncio.create_task(self._handle_item(item))
        logger.debug("Poll cycle complete (queue implementation pending)")

    async def _handle_item(self, item: object) -> None:
        """Full lifecycle for a single claimed work item."""
        # TODO (Phase 1): implement dispatch, heartbeat, and status reporting
        logger.info("Handling item: %s", item)

    def _invoke_shell_bridge(self, subcommand: str, args: str = "") -> int:
        """Invoke the devcontainer shell bridge script (ADR-07).

        Args:
            subcommand: One of 'up', 'start', 'prompt'.
            args: Additional arguments (e.g. the prompt string for 'prompt').

        Returns:
            Process exit code.
        """
        script = Path(SHELL_BRIDGE_SCRIPT)
        if not script.exists():
            logger.error("Shell bridge not found: %s", script)
            return 1

        cmd = [str(script), subcommand]
        if args:
            cmd.append(args)

        logger.info("Shell bridge: %s %s", subcommand, args[:80] if args else "")
        result = subprocess.run(cmd, capture_output=False)  # noqa: S603
        return result.returncode


def main() -> None:
    """Entry point for the Sentinel service."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [sentinel:%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    sentinel = SentinelOrchestrator()
    try:
        asyncio.run(sentinel.run())
    except KeyboardInterrupt:
        logger.info("Sentinel stopped by keyboard interrupt")


if __name__ == "__main__":
    main()
