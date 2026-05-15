from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query, status

from app.config import get_settings
from app.log_store import fetch_logs, fetch_trace_logs

router = APIRouter(prefix="/admin/traces", tags=["traces"])


def _verify_log_viewer_key(x_log_viewer_key: str | None) -> None:
    settings = get_settings()
    if settings.log_viewer_api_key and x_log_viewer_key != settings.log_viewer_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid log viewer API key",
        )


@router.get("")
async def list_recent_traces(
    limit: int = Query(default=20, ge=1, le=100),
    x_log_viewer_key: str | None = Header(default=None),
) -> dict[str, Any]:
    _verify_log_viewer_key(x_log_viewer_key)
    settings = get_settings()
    logs = fetch_logs(settings.log_db_path, limit=500)
    traces: dict[str, dict[str, Any]] = {}

    for log in logs:
        trace_id = log.get("trace_id")
        if not trace_id:
            continue
        trace = traces.setdefault(
            trace_id,
            {
                "trace_id": trace_id,
                "first_seen": log["timestamp"],
                "last_seen": log["timestamp"],
                "event_count": 0,
                "status_code": None,
                "path": None,
                "method": None,
            },
        )
        trace["event_count"] += 1
        trace["first_seen"] = min(trace["first_seen"], log["timestamp"])
        trace["last_seen"] = max(trace["last_seen"], log["timestamp"])
        if log.get("event") == "request_completed":
            trace["status_code"] = log.get("status_code")
            trace["path"] = log.get("path")
            trace["method"] = log.get("method")

    return {
        "count": min(len(traces), limit),
        "traces": list(traces.values())[:limit],
    }


@router.get("/{trace_id}")
async def get_trace(
    trace_id: str,
    x_log_viewer_key: str | None = Header(default=None),
) -> dict[str, Any]:
    _verify_log_viewer_key(x_log_viewer_key)
    settings = get_settings()
    logs = fetch_trace_logs(settings.log_db_path, trace_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Trace not found")

    request_log = next(
        (log for log in logs if log.get("event") == "request_completed"),
        logs[-1],
    )
    first_timestamp = logs[0]["timestamp"]
    last_timestamp = request_log.get("timestamp") or logs[-1]["timestamp"]
    root_span = {
        "name": request_log.get("span_name")
        or f"HTTP {request_log.get('method')} {request_log.get('path')}",
        "kind": "server",
        "start_time": first_timestamp,
        "end_time": last_timestamp,
        "duration_ms": request_log.get("duration_ms"),
        "status": _span_status(request_log.get("status_code")),
        "attributes": {
            "http.method": request_log.get("method"),
            "http.route": request_log.get("path"),
            "http.status_code": request_log.get("status_code"),
            "client.address": request_log.get("client_ip"),
            "request.id": request_log.get("request_id"),
        },
    }

    return {
        "trace_id": trace_id,
        "service": {
            "name": settings.app_name,
            "environment": settings.app_env,
        },
        "generated_at": datetime.now(UTC).isoformat(),
        "root_span": root_span,
        "events": [_to_trace_event(log) for log in logs],
    }


def _span_status(status_code: int | None) -> str:
    if status_code is None:
        return "unknown"
    if status_code >= 500:
        return "error"
    if status_code >= 400:
        return "client_error"
    return "ok"


def _to_trace_event(log: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": log["timestamp"],
        "level": log["level"],
        "event": log["event"],
        "span_name": log.get("span_name"),
        "logger": log["logger"],
        "message": log["message"],
        "attributes": log["details"],
    }
