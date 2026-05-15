import json
import logging
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LOG_RECORD_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


def initialize_log_store(db_path: str) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS application_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                logger TEXT NOT NULL,
                event TEXT NOT NULL,
                message TEXT NOT NULL,
                method TEXT,
                path TEXT,
                status_code INTEGER,
                duration_ms REAL,
                client_ip TEXT,
                request_id TEXT,
                trace_id TEXT,
                span_name TEXT,
                action TEXT,
                resource TEXT,
                resource_id TEXT,
                details TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_application_logs_timestamp ON application_logs(timestamp)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_application_logs_event ON application_logs(event)"
        )
        _ensure_column(connection, "application_logs", "trace_id", "TEXT")
        _ensure_column(connection, "application_logs", "span_name", "TEXT")
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_application_logs_trace_id ON application_logs(trace_id)"
        )


def _ensure_column(
    connection: sqlite3.Connection,
    table_name: str,
    column_name: str,
    column_type: str,
) -> None:
    columns = {
        row[1]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name not in columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")


def _json_default(value: Any) -> str:
    return str(value)


def record_to_row(record: logging.LogRecord) -> dict[str, Any]:
    details = {
        key: value
        for key, value in record.__dict__.items()
        if key not in LOG_RECORD_FIELDS and not key.startswith("_")
    }
    event = details.get("event") or record.getMessage()

    return {
        "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
        "level": record.levelname,
        "logger": record.name,
        "event": str(event),
        "message": record.getMessage(),
        "method": details.get("method"),
        "path": details.get("path"),
        "status_code": details.get("status_code"),
        "duration_ms": details.get("duration_ms"),
        "client_ip": details.get("client_ip"),
        "request_id": details.get("request_id"),
        "trace_id": details.get("trace_id"),
        "span_name": details.get("span_name"),
        "action": details.get("action"),
        "resource": details.get("resource"),
        "resource_id": details.get("resource_id"),
        "details": json.dumps(details, default=_json_default, ensure_ascii=True),
    }


class SQLiteLogHandler(logging.Handler):
    def __init__(self, db_path: str) -> None:
        super().__init__()
        self.db_path = db_path
        initialize_log_store(db_path)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            row = record_to_row(record)
            with sqlite3.connect(self.db_path) as connection:
                connection.execute(
                    """
                    INSERT INTO application_logs (
                        timestamp, level, logger, event, message, method, path,
                        status_code, duration_ms, client_ip, request_id, trace_id,
                        span_name, action, resource, resource_id, details
                    )
                    VALUES (
                        :timestamp, :level, :logger, :event, :message, :method, :path,
                        :status_code, :duration_ms, :client_ip, :request_id, :trace_id,
                        :span_name, :action, :resource, :resource_id, :details
                    )
                    """,
                    row,
                )
        except Exception:
            self.handleError(record)


def fetch_logs(
    db_path: str,
    *,
    limit: int = 100,
    event: str | None = None,
    level: str | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
    order: str = "DESC",
) -> list[dict[str, Any]]:
    initialize_log_store(db_path)
    filters: list[str] = []
    params: dict[str, Any] = {"limit": limit}

    if event:
        filters.append("event = :event")
        params["event"] = event
    if level:
        filters.append("level = :level")
        params["level"] = level.upper()
    if request_id:
        filters.append("request_id = :request_id")
        params["request_id"] = request_id
    if trace_id:
        filters.append("trace_id = :trace_id")
        params["trace_id"] = trace_id

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    order_direction = "ASC" if order.upper() == "ASC" else "DESC"

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            f"""
            SELECT
                id, timestamp, level, logger, event, message, method, path,
                status_code, duration_ms, client_ip, request_id, trace_id,
                span_name, action, resource, resource_id, details
            FROM application_logs
            {where_clause}
            ORDER BY id {order_direction}
            LIMIT :limit
            """,
            params,
        ).fetchall()

    logs = []
    for row in rows:
        log = dict(row)
        log["details"] = json.loads(log["details"])
        logs.append(log)
    return logs


def fetch_trace_logs(db_path: str, trace_id: str) -> list[dict[str, Any]]:
    return fetch_logs(db_path, limit=500, trace_id=trace_id, order="ASC")
