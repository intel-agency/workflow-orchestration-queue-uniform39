"""Notifier service package.

FastAPI webhook receiver — The Ear. Validates incoming GitHub webhook payloads,
parses events into WorkItem models, and queues them for the Sentinel.
"""
