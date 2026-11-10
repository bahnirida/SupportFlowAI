from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class TicketRead(TicketCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
