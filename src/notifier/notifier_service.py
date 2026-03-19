"""Notifier Service — FastAPI webhook receiver (The Ear).

Exposes /webhooks/github to securely receive GitHub App events.
Validates HMAC SHA-256 signatures, parses payloads into WorkItem models,
and applies agent:queued labels to trigger the Sentinel.

Architecture: see plan_docs/architecture.md — Pillar 1: The Ear.
Security: HMAC verification occurs BEFORE any JSON parsing (prevents
          prompt injection via webhook spoofing).

Usage:
    uv run uvicorn notifier.notifier_service:app --host 0.0.0.0 --port 8000
    # or via project script:
    uv run notifier
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI(
    title="workflow-orchestration-queue Notifier",
    description="Secure webhook receiver for GitHub App events",
    version="0.1.0",
)

WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")


# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------


def _verify_signature(payload_bytes: bytes, signature_header: str | None) -> bool:
    """Validate the X-Hub-Signature-256 HMAC header.

    Must be called BEFORE any JSON parsing to prevent prompt injection attacks.

    Args:
        payload_bytes: Raw request body bytes.
        signature_header: Value of the X-Hub-Signature-256 header.

    Returns:
        True if the signature is valid; False otherwise.
    """
    if not signature_header or not WEBHOOK_SECRET:
        return False
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload_bytes, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------


class WebhookAck(BaseModel):
    """Response body returned for accepted webhook events."""

    accepted: bool = True
    message: str = "Event received"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.post("/webhooks/github", response_model=WebhookAck, status_code=202)
async def receive_github_webhook(request: Request) -> WebhookAck:
    """Receive and validate a GitHub App webhook event.

    Security: HMAC signature is verified before the request body is parsed.
    Invalid or missing signatures are rejected with HTTP 401.

    Returns:
        WebhookAck with HTTP 202 Accepted for valid, recognised events.

    Raises:
        HTTPException 401: If the HMAC signature is missing or invalid.
    """
    payload_bytes = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    # SECURITY: verify signature BEFORE parsing — prevents prompt injection
    if not _verify_signature(payload_bytes, signature):
        logger.warning("Invalid or missing webhook signature from %s", request.client)
        raise HTTPException(status_code=401, detail="Invalid or missing HMAC signature")

    event_type = request.headers.get("X-GitHub-Event", "unknown")
    logger.info("Received GitHub event: %s", event_type)

    # TODO (Phase 2): parse payload into WorkItem and apply agent:queued label
    # payload = json.loads(payload_bytes)
    # work_item = _triage_event(event_type, payload)
    # if work_item:
    #     await queue.apply_queued_label(work_item)

    return WebhookAck(message=f"Event '{event_type}' received")


@app.get("/health")
async def health_check() -> JSONResponse:
    """Liveness probe endpoint."""
    return JSONResponse({"status": "ok"})


def main() -> None:
    """Entry point for the Notifier service."""
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))  # noqa: S104


if __name__ == "__main__":
    main()
