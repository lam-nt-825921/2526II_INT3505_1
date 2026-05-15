import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.config import get_settings
from app.logging_config import configure_logging
from app.metrics import setup_metrics
from app.rate_limit import limiter
from app.routes import external, health, items, logs, traces
from app.trace_context import extract_trace_id, traceparent_from_trace_id

settings = get_settings()
configure_logging(settings.log_level, settings.log_db_path)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Week 10 demo API for deployment, observability and production security basics.",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        trace_id = extract_trace_id(request.headers.get("traceparent"))
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        start = time.perf_counter()

        logger.info(
            "request_started",
            extra={
                "event": "request_started",
                "span_name": f"HTTP {request.method} {request.url.path}",
                "request_id": request_id,
                "trace_id": trace_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": get_remote_address(request),
            },
        )

        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        response.headers["traceparent"] = traceparent_from_trace_id(trace_id)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "span_name": f"HTTP {request.method} {request.url.path}",
                "request_id": request_id,
                "trace_id": trace_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "client_ip": get_remote_address(request),
            },
        )
        return response

    app.include_router(health.router)
    app.include_router(items.router)
    app.include_router(external.router)
    app.include_router(logs.router)
    app.include_router(traces.router)
    setup_metrics(app)

    return app


async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(
        "rate_limit_exceeded",
        extra={
            "event": "rate_limit_exceeded",
            "path": request.url.path,
            "client_ip": get_remote_address(request),
            "limit": str(exc.detail),
            "request_id": getattr(request.state, "request_id", None),
            "trace_id": getattr(request.state, "trace_id", None),
            "span_name": f"HTTP {request.method} {request.url.path}",
        },
    )
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded", "limit": str(exc.detail)},
    )


app = create_app()
