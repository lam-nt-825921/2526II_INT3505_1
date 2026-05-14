from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=240)


class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class ExternalStatusResponse(BaseModel):
    status: str
    source: str
