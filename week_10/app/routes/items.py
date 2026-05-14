from uuid import UUID

from fastapi import APIRouter, Request, status

from app.audit import write_audit_event
from app.config import get_settings
from app.metrics import items_created_total
from app.rate_limit import limiter
from app.schemas import Item, ItemCreate

router = APIRouter(prefix="/api/v1/items", tags=["items"])

items_store: dict[UUID, Item] = {}


@router.get("", response_model=list[Item])
async def list_items() -> list[Item]:
    return list(items_store.values())


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
@limiter.limit(lambda: get_settings().rate_limit_write)
async def create_item(request: Request, payload: ItemCreate) -> Item:
    item = Item(name=payload.name, description=payload.description)
    items_store[item.id] = item
    items_created_total.inc()
    write_audit_event(
        request=request,
        action="item_created",
        resource="item",
        resource_id=str(item.id),
        metadata={"name": item.name},
    )
    return item
