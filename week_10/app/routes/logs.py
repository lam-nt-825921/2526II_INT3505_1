from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query, status

from app.config import get_settings
from app.log_store import fetch_logs

router = APIRouter(prefix="/admin/logs", tags=["logs"])


@router.get("")
async def list_application_logs(
    limit: int = Query(default=100, ge=1, le=500),
    event: str | None = None,
    level: str | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
    x_log_viewer_key: str | None = Header(default=None),
) -> dict[str, Any]:
    settings = get_settings()
    if settings.log_viewer_api_key and x_log_viewer_key != settings.log_viewer_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid log viewer API key",
        )

    logs = fetch_logs(
        settings.log_db_path,
        limit=limit,
        event=event,
        level=level,
        request_id=request_id,
        trace_id=trace_id,
    )
    return {
        "count": len(logs),
        "logs": logs,
    }
