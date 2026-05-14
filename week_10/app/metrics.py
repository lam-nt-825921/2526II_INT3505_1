from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

items_created_total = Counter(
    "items_created_total",
    "Total number of demo items created.",
)


def setup_metrics(app) -> None:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
