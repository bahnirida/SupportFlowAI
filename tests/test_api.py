import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Imports and non-database tests do not require a local PostgreSQL server.
os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://supportflow:unused@localhost/supportflow"
)

from app.db.session import get_db
from app.main import app


def test_health_and_validation():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.post("/tickets", json={"title": "", "description": ""}).status_code == 422
        assert client.get("/tickets/not-a-uuid").status_code == 422


def test_ticket_lifecycle_postgresql():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to a migrated PostgreSQL test database")

    engine = create_engine(url, connect_args={"connect_timeout": 5})
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
            def override_db():
                yield session

            app.dependency_overrides[get_db] = override_db
            try:
                with TestClient(app) as client:
                    assert client.get("/health/db").status_code == 200
                    response = client.post("/tickets", json={
                        "title": "Cannot log in", "description": "Please help me sign in."
                    })
                    assert response.status_code == 201
                    ticket = response.json()
                    assert ticket["status"] == "open"
                    session.expunge_all()
                    assert client.get(f"/tickets/{ticket['id']}").json() == ticket
                    assert ticket in client.get("/tickets").json()
                    assert client.get(f"/tickets/{uuid4()}").status_code == 404
            finally:
                app.dependency_overrides.clear()
        transaction.rollback()
    engine.dispose()
