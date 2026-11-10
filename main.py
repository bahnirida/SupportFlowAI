from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

import testdb

app = FastAPI(title="SupportFlowAI")


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class Ticket(TicketCreate):
    id: UUID
    status: str = "open"


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/tickets", response_model=Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(payload: TicketCreate):
    return testdb.create_ticket(uuid4(), payload.title, payload.description)


@app.get("/tickets", response_model=list[Ticket])
async def list_tickets():
    return testdb.list_tickets()


@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: UUID):
    ticket = testdb.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
