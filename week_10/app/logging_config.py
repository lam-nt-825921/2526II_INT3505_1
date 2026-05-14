import logging
import sys

from pythonjsonlogger import jsonlogger

from app.log_store import SQLiteLogHandler


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        if "event" not in log_record:
            log_record["event"] = record.getMessage()


def configure_logging(log_level: str, log_db_path: str | None = None) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(log_level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter(
            "%(asctime)s %(level)s %(name)s %(event)s",
            rename_fields={"asctime": "timestamp"},
        )
    )

    root.addHandler(handler)

    if log_db_path:
        sqlite_handler = SQLiteLogHandler(log_db_path)
        sqlite_handler.setLevel(log_level.upper())
        root.addHandler(sqlite_handler)

    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").setLevel(log_level.upper())
