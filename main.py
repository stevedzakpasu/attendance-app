import re
from fastapi import FastAPI, Depends, Query, HTTPException
from typing import List
import services as _services
import models as _models
from sqlmodel import Session, select
import schemas as _schemas


tags_metadata = [
    {
        "name": "members",
        "description": "Operations with **members**",
    },
    {
        "name": "halls",
        "description": "Operations with **halls**",
    },
    {
        "name": "programmes",
        "description": "Operations with **programmes**",
    },
    {
        "name": "levels",
        "description": "Operations with **levels**",
    },
    {
        "name": "congregations",
        "description": "Operations with **congregations**",
    },
    {
        "name": "committees",
        "description": "Operations with **committees**",
    },
    {
        "name": "events",
        "description": "Operations with **events**",
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.on_event("startup")
def on_startup():
    _services.create_db_and_tables()


@app.post("/api/members/", tags=["members"], response_model=_schemas.MemberCreate)
def create_member(*, session: Session = Depends(_services.get_session), member: _schemas.MemberCreate):
    db_member = _models.Member.from_orm(member)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@ app.get("/api/members/",  tags=["members"], response_model=List[_schemas.MemberReadWithEvents])
def read_members(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    members = session.exec(
        select(_models.Member).offset(offset).limit(limit)).all()
    return members


@app.get("/api/members/{member_id}",  tags=["members"], response_model=_schemas.MemberReadWithEvents)
def read_hero(*, session: Session = Depends(_services.get_session), member_id: int):
    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@app.patch("/api/members/{member_id}",  tags=["members"], response_model=_schemas.MemberReadWithEvents)
def update_member(
    *, session: Session = Depends(_services.get_session), member_id: int, member: _schemas.MemberUpdate
):
    db_member = session.get(_models.Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    member_data = member.dict(exclude_unset=True)
    for key, value in member_data.items():
        setattr(db_member, key, value)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@app.delete("/api/members/{member_id}",  tags=["members"])
def delete_member(*, session: Session = Depends(_services.get_session), member_id: int):

    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    session.delete(member)
    session.commit()
    return {"ok": True}


@app.post("/api/halls/", tags=["halls"], response_model=_schemas.InfoCreate)
def create_hall(*, session: Session = Depends(_services.get_session), hall: _schemas.InfoCreate):
    db_hall = _models.Member.from_orm(hall)
    session.add(db_hall)
    session.commit()
    session.refresh(db_hall)
    return db_hall


@ app.get("/api/halls/",  tags=["halls"], response_model=List[_schemas.InfoRead])
def read_halls(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    halls = session.exec(
        select(_models.Hall).offset(offset).limit(limit)).all()
    return halls


@app.get("/api/halls/{hall_id}",  tags=["halls"], response_model=_schemas.InfoRead)
def read_hall(*, session: Session = Depends(_services.get_session), hall_id: int):
    hall = session.get(_models.Hall, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall


@app.patch("/api/halls/{hall_id}",  tags=["halls"], response_model=_schemas.InfoRead)
def update_hall(
    *, session: Session = Depends(_services.get_session), hall_id: int, hall: _schemas.InfoUpdate
):
    db_hall = session.get(_models.Hall, hall_id)
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    hall_data = hall.dict(exclude_unset=True)
    for key, value in hall_data.items():
        setattr(db_hall, key, value)
    session.add(db_hall)
    session.commit()
    session.refresh(db_hall)
    return db_hall


@app.delete("/api/halls/{hall_id}",  tags=["halls"])
def delete_hall(*, session: Session = Depends(_services.get_session), hall_id: int):

    hall = session.get(_models.Hall, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    session.delete(hall)
    session.commit()
    return {"ok": True}


@app.post("/api/programmes/", tags=["programmes"], response_model=_schemas.InfoCreate)
def create_programme(*, session: Session = Depends(_services.get_session), programme: _schemas.InfoCreate):
    db_programme = _models.Programme.from_orm(programme)
    session.add(db_programme)
    session.commit()
    session.refresh(db_programme)
    return db_programme


@ app.get("/api/programmes/",  tags=["programmes"], response_model=List[_schemas.InfoRead])
def read_programmes(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    programmes = session.exec(
        select(_models.Programme).offset(offset).limit(limit)).all()
    return programmes


@app.get("/api/programmes/{programme_id}",  tags=["programmes"], response_model=_schemas.InfoRead)
def read_programmes(*, session: Session = Depends(_services.get_session), programme_id: int):
    programme = session.get(_models.Programme, programme_id)
    if not programme:
        raise HTTPException(status_code=404, detail="Programme not found")
    return programme


@app.patch("/api/programmes/{programme_id}",  tags=["programmes"], response_model=_schemas.InfoRead)
def update_program(
    *, session: Session = Depends(_services.get_session), programme_id: int, programme: _schemas.InfoUpdate
):
    db_programme = session.get(_models.Programme, programme_id)
    if not db_programme:
        raise HTTPException(status_code=404, detail="Programme not found")
    programme_data = programme.dict(exclude_unset=True)
    for key, value in programme_data.items():
        setattr(db_programme, key, value)
    session.add(db_programme)
    session.commit()
    session.refresh(db_programme)
    return db_programme


@app.delete("/api/programmes/{programme_id}",  tags=["programmes"])
def delete_programme(*, session: Session = Depends(_services.get_session), programme_id: int):

    programme = session.get(_models.Programme, programme_id)
    if not programme:
        raise HTTPException(status_code=404, detail="Programne not found")
    session.delete(programme)
    session.commit()
    return {"ok": True}


@app.post("/api/levels/", tags=["levels"], response_model=_schemas.InfoCreate)
def create_level(*, session: Session = Depends(_services.get_session), level: _schemas.InfoCreate):
    db_level = _models.Level.from_orm(level)
    session.add(db_level)
    session.commit()
    session.refresh(db_level)
    return db_level


@ app.get("/api/levels/",  tags=["levels"], response_model=List[_schemas.InfoRead])
def read_level(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    levels = session.exec(
        select(_models.Level).offset(offset).limit(limit)).all()
    return levels


@app.get("/api/levels/{level_id}",  tags=["levels"], response_model=_schemas.InfoRead)
def read_levels(*, session: Session = Depends(_services.get_session), level_id: int):
    level = session.get(_models.Level, level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level


@app.patch("/api/levels/{level_id}",  tags=["levels"], response_model=_schemas.InfoRead)
def update_level(
    *, session: Session = Depends(_services.get_session), level_id: int, level: _schemas.InfoUpdate
):
    db_level = session.get(_models.Level, level_id)
    if not db_level:
        raise HTTPException(status_code=404, detail="Level not found")
    level_data = level.dict(exclude_unset=True)
    for key, value in level_data.items():
        setattr(db_level, key, value)
    session.add(db_level)
    session.commit()
    session.refresh(db_level)
    return db_level


@app.delete("/api/levels/{level_id}",  tags=["levels"])
def delete_level(*, session: Session = Depends(_services.get_session), level_id: int):

    level = session.get(_models.Programme, level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    session.delete(level)
    session.commit()
    return {"ok": True}


@app.post("/api/congregations/", tags=["congregations"], response_model=_schemas.InfoCreate)
def create_congregation(*, session: Session = Depends(_services.get_session), congregation: _schemas.InfoCreate):
    db_congregation = _models.Congregation.from_orm(congregation)
    session.add(db_congregation)
    session.commit()
    session.refresh(db_congregation)
    return db_congregation


@ app.get("/api/congregations/",  tags=["congregations"], response_model=List[_schemas.InfoRead])
def read_congregation(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    congregations = session.exec(
        select(_models.Congregation).offset(offset).limit(limit)).all()
    return congregations


@app.get("/api/congregations/{congregation_id}",  tags=["congregations"], response_model=_schemas.InfoRead)
def read_congregations(*, session: Session = Depends(_services.get_session), congregation_id: int):
    congregation = session.get(_models.Congregation, congregation_id)
    if not congregation:
        raise HTTPException(status_code=404, detail="Congregation not found")
    return congregation


@app.patch("/api/congregations/{congregation_id}",  tags=["congregations"], response_model=_schemas.InfoRead)
def update_congregation(
    *, session: Session = Depends(_services.get_session), congregation_id: int, congregation: _schemas.InfoUpdate
):
    db_congregation = session.get(_models.Congregation, congregation_id)
    if not db_congregation:
        raise HTTPException(status_code=404, detail="Congregation not found")
    congregation_data = congregation.dict(exclude_unset=True)
    for key, value in congregation_data.items():
        setattr(db_congregation, key, value)
    session.add(db_congregation)
    session.commit()
    session.refresh(db_congregation)
    return db_congregation


@app.delete("/api/congregations/{congregation_id}",  tags=["congregations"])
def delete_congregation(*, session: Session = Depends(_services.get_session), congregation_id: int):

    congregation = session.get(_models.Congregation, congregation_id)
    if not congregation:
        raise HTTPException(status_code=404, detail="Congregation not found")
    session.delete(congregation)
    session.commit()
    return {"ok": True}


@app.post("/api/committees/", tags=["committees"], response_model=_schemas.InfoCreate)
def create_committee(*, session: Session = Depends(_services.get_session), committee: _schemas.InfoCreate):
    db_committee = _models.Congregation.from_orm(committee)
    session.add(db_committee)
    session.commit()
    session.refresh(db_committee)
    return db_committee


@ app.get("/api/committees/",  tags=["committees"], response_model=List[_schemas.InfoRead])
def read_committee(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    committees = session.exec(
        select(_models.Committee).offset(offset).limit(limit)).all()
    return committees


@app.get("/api/committees/{congregation_id}",  tags=["committees"], response_model=_schemas.InfoRead)
def read_committees(*, session: Session = Depends(_services.get_session), committee_id: int):
    committee = session.get(_models.Congregation, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    return committee


@app.patch("/api/committees/{committee_id}",  tags=["committees"], response_model=_schemas.InfoRead)
def update_committee(
    *, session: Session = Depends(_services.get_session), committee_id: int, committee: _schemas.InfoUpdate
):
    db_committee = session.get(_models.Committee, committee_id)
    if not db_committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    committee_data = committee.dict(exclude_unset=True)
    for key, value in committee_data.items():
        setattr(db_committee, key, value)
    session.add(db_committee)
    session.commit()
    session.refresh(db_committee)
    return db_committee


@app.delete("/api/committees/{committee_id}",  tags=["committees"])
def delete_committee(*, session: Session = Depends(_services.get_session), committee_id: int):

    committee = session.get(_models.Committee, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    session.delete(committee)
    session.commit()
    return {"ok": True}


@app.post("/api/events/", tags=["events"], response_model=_schemas.EventCreate)
def create_event(*, session: Session = Depends(_services.get_session), event: _schemas.EventCreate):
    db_event = _models.Congregation.from_orm(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@ app.get("/api/events/",  tags=["events"], response_model=List[_schemas.EventReadWithMembers])
def read_event(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    events = session.exec(
        select(_models.Event).offset(offset).limit(limit)).all()
    return events


@app.get("/api/events/{event_id}",  tags=["events"], response_model=_schemas.EventReadWithMembers)
def read_events(*, session: Session = Depends(_services.get_session), event_id: int):
    event = session.get(_models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.patch("/api/events/{event_id}",  tags=["events"], response_model=_schemas.EventReadWithMembers)
def update_event(
    *, session: Session = Depends(_services.get_session), event_id: int, event: _schemas.EventUpdate
):
    db_event = session.get(_models.Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    committee_data = event.dict(exclude_unset=True)
    for key, value in committee_data.items():
        setattr(db_event, key, value)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@app.delete("/api/events/{event_id}",  tags=["events"])
def delete_event(*, session: Session = Depends(_services.get_session), event_id: int):

    event = session.get(_models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return {"ok": True}


@app.post("/api/events/{event_id}/add_attendee",  tags=["events"])
def add_attendee(*, session: Session = Depends(_services.get_session), event_id: int, member_id: int):
    attendee = session.exec(
        select(_models.Member).where(_models.Member.id == member_id)
    ).one()
    event = session.get(_models.Event, event_id)
    event.members_attended.append(attendee)
    session.add(event)
    session.commit()
    return ({"ok": True})
