from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import ticket as repository
from app.schemas.ticket import TicketCreate, TicketRead

router = APIRouter(prefix="/tickets", tags=["tickets"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: DatabaseSession):
    return repository.create_ticket(db, payload)


@router.get("", response_model=list[TicketRead])
def list_tickets(db: DatabaseSession):
    return repository.list_tickets(db)


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: UUID, db: DatabaseSession):
    ticket = repository.get_ticket(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
