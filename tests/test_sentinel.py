"""Tests for the Sentinel Orchestrator."""
from __future__ import annotations

import pytest
from src.sentinel.orchestrator_sentinel import SentinelOrchestrator


def test_sentinel_initialises_with_generated_id() -> None:
    sentinel = SentinelOrchestrator()
    assert sentinel.sentinel_id is not None
    assert len(sentinel.sentinel_id) > 0


def test_sentinel_accepts_explicit_id() -> None:
    sentinel = SentinelOrchestrator(sentinel_id="test-sentinel-01")
    assert sentinel.sentinel_id == "test-sentinel-01"


def test_sentinel_stop_sets_running_false() -> None:
    sentinel = SentinelOrchestrator()
    sentinel._running = True
    sentinel.stop()
    assert sentinel._running is False


@pytest.mark.asyncio
async def test_poll_cycle_does_not_raise() -> None:
    """Poll cycle completes without error (queue implementation pending)."""
    sentinel = SentinelOrchestrator()
    await sentinel._poll_cycle()  # should not raise
