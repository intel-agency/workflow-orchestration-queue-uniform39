"""Tests for the FastAPI webhook Notifier service.

TC-01: Invalid HMAC signature → 401 Unauthorized (no JSON parsing)
TC-02: Valid webhook → 202 Accepted (with correct event processing)
"""
from __future__ import annotations

import hashlib
import hmac
import os

import pytest
from fastapi.testclient import TestClient

# Set a test webhook token before importing the app
_TEST_WEBHOOK_TOKEN = "test-webhook-token-for-unit-tests-only"  # noqa: S105
os.environ["WEBHOOK_SECRET"] = _TEST_WEBHOOK_TOKEN

from src.notifier.notifier_service import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _sign_payload(payload: bytes, secret: str = _TEST_WEBHOOK_TOKEN) -> str:
    """Generate a valid X-Hub-Signature-256 header value."""
    sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


def test_tc01_invalid_signature_returns_401(client: TestClient) -> None:
    """TC-01: Request with invalid HMAC signature is rejected with 401."""
    payload = b'{"action": "opened"}'
    response = client.post(
        "/webhooks/github",
        content=payload,
        headers={
            "X-GitHub-Event": "issues",
            "X-Hub-Signature-256": "sha256=invalidsignature",
        },
    )
    assert response.status_code == 401


def test_missing_signature_returns_401(client: TestClient) -> None:
    """Request without X-Hub-Signature-256 header is rejected with 401."""
    payload = b'{"action": "opened"}'
    response = client.post(
        "/webhooks/github",
        content=payload,
        headers={"X-GitHub-Event": "issues"},
    )
    assert response.status_code == 401


def test_tc02_valid_signature_returns_202(client: TestClient) -> None:
    """TC-02: Request with valid HMAC signature returns 202 Accepted."""
    payload = b'{"action": "opened", "issue": {"number": 1}}'
    signature = _sign_payload(payload)
    response = client.post(
        "/webhooks/github",
        content=payload,
        headers={
            "X-GitHub-Event": "issues",
            "X-Hub-Signature-256": signature,
        },
    )
    assert response.status_code == 202
    data = response.json()
    assert data["accepted"] is True


def test_health_endpoint(client: TestClient) -> None:
    """Health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
