from fastapi import FastAPI, Depends, Query, HTTPException
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
def create_member(*, session: Session = Depends(_services.get_session), member: _schemas.MemberCreate):
    db_member = _models.Member.from_orm(member)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@ app.get("/api/members/", response_model=List[_schemas.MemberRead])
def read_members(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    members = session.exec(
        select(_models.Member).offset(offset).limit(limit)).all()
    return members


@app.get("/api/members/{member_id}", response_model=_schemas.MemberRead)
def read_hero(*, session: Session = Depends(_services.get_session), member_id: int):
    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# def update_heroes(id):
#     with Session(_database.engine) as session:
#         statement = select(_models.Member).where(_models.Member.name == id)  #
#         results = session.exec(statement)  #
#         hero_1 = results.one()  #
#         print("Hero 1:", hero_1)  #
