from fastapi import FastAPI
import services as _services
import database as _database
import models as _models
from sqlmodel import Session
import schemas as _schemas

app = FastAPI()


@app.on_event("startup")
def on_startup():
    _services.create_db_and_tables()


@app.post("/members/", response_model=_schemas.MemberCreate)
def create_member(member: _schemas.MemberCreate):
    with Session(_database.engine) as session:
        db_member = _models.Member.from_orm(member)
        session.add(db_member)
        session.commit()
        session.refresh(db_member)
        return db_member


# @ app.get("/heroes/", response_model = List[HeroRead])
# def read_heroes():
#     with Session(engine) as session:
#         heroes=session.exec(select(Hero)).all()
#         return heroes
