from uuid import uuid4


def extract_trace_id(traceparent: str | None) -> str:
    if traceparent:
        parts = traceparent.split("-")
        if len(parts) == 4 and len(parts[1]) == 32:
            trace_id = parts[1].lower()
            if all(character in "0123456789abcdef" for character in trace_id):
                return trace_id
    return uuid4().hex


def traceparent_from_trace_id(trace_id: str) -> str:
    return f"00-{trace_id}-{uuid4().hex[:16]}-01"
