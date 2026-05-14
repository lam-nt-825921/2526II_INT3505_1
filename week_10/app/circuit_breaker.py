import logging

import httpx
import pybreaker

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CircuitBreakerLogger(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.warning(
            "circuit_state_changed",
            extra={
                "event": "circuit_state_changed",
                "circuit": cb.name,
                "old_state": old_state.name,
                "new_state": new_state.name,
            },
        )


external_service_breaker = pybreaker.CircuitBreaker(
    fail_max=settings.circuit_fail_max,
    reset_timeout=settings.circuit_reset_timeout_seconds,
    name="external_service",
    listeners=[CircuitBreakerLogger()],
)


@external_service_breaker
def fetch_external_status() -> dict[str, str]:
    current_settings = get_settings()
    if current_settings.external_failure_mode:
        raise httpx.ConnectError("EXTERNAL_FAILURE_MODE is enabled")

    with httpx.Client(timeout=3.0) as client:
        response = client.get(current_settings.external_service_url)
    response.raise_for_status()

    return {"status": "ok", "source": current_settings.external_service_url}
