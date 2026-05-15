import logging
from datetime import UTC, datetime
from typing import Any

from fastapi import Request

audit_logger = logging.getLogger("audit")


def write_audit_event(
    request: Request,
    action: str,
    resource: str,
    resource_id: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    audit_logger.info(
        "audit_event",
        extra={
            "event": "audit_event",
            "action": action,
            "resource": resource,
            "resource_id": resource_id,
            "client_ip": request.client.host if request.client else "unknown",
            "request_id": getattr(request.state, "request_id", None),
            "trace_id": getattr(request.state, "trace_id", None),
            "span_name": "audit.write",
            "audit_timestamp": datetime.now(UTC).isoformat(),
            "metadata": metadata or {},
        },
    )
