import logging

import pybreaker
from fastapi import APIRouter, HTTPException, Request, status
from httpx import HTTPError

from app.circuit_breaker import fetch_external_status
from app.config import get_settings
from app.rate_limit import limiter
from app.schemas import ExternalStatusResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/external", tags=["external"])


@router.get("/status", response_model=ExternalStatusResponse)
@limiter.limit(lambda: get_settings().rate_limit_external)
async def external_status(request: Request) -> ExternalStatusResponse:
    logger.info(
        "external_call_started",
        extra={
            "event": "external_call_started",
            "span_name": "external.status",
            "path": str(request.url.path),
            "request_id": getattr(request.state, "request_id", None),
            "trace_id": getattr(request.state, "trace_id", None),
        },
    )
    try:
        result = fetch_external_status()
    except pybreaker.CircuitBreakerError as exc:
        logger.warning(
            "external_circuit_open",
            extra={
                "event": "external_circuit_open",
                "span_name": "external.status",
                "path": str(request.url.path),
                "request_id": getattr(request.state, "request_id", None),
                "trace_id": getattr(request.state, "trace_id", None),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service circuit is open",
        ) from exc
    except HTTPError as exc:
        logger.warning(
            "external_service_failed",
            extra={
                "event": "external_service_failed",
                "span_name": "external.status",
                "path": str(request.url.path),
                "error": str(exc),
                "request_id": getattr(request.state, "request_id", None),
                "trace_id": getattr(request.state, "trace_id", None),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service is unavailable",
        ) from exc

    logger.info(
        "external_call_completed",
        extra={
            "event": "external_call_completed",
            "span_name": "external.status",
            "path": str(request.url.path),
            "request_id": getattr(request.state, "request_id", None),
            "trace_id": getattr(request.state, "trace_id", None),
            "source": result["source"],
        },
    )
    return ExternalStatusResponse(**result)
