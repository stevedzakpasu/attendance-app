from fastapi import FastAPI
from typing import List
import services as _services
import database as _database
import models as _models
from sqlmodel import Session, select
import schemas as _schemas

app = FastAPI()


@app.on_event("startup")
def on_startup():
    _services.create_db_and_tables()


@app.post("/api/members/", response_model=_schemas.MemberCreate)
def create_member(member: _schemas.MemberCreate):
    with Session(_database.engine) as session:
        db_member = _models.Member.from_orm(member)
        session.add(db_member)
        session.commit()
        session.refresh(db_member)
        return db_member


@ app.get("/api/members/", response_model=List[_schemas.MemberRead])
def read_members():
    with Session(_database.engine) as session:
        members = session.exec(select(_models.Member)).all()
        return members
