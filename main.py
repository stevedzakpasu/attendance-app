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
        "name": "committees",
        "description": "Operations with **committees**",
    },
    {
        "name": "events",
        "description": "Operations with **events**",
    },
    {
        "name": "categories",
        "description": "Operations with **categories**",
    },
    {
        "name": "semesters",
        "description": "Operations with **semesters**",
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
def read_member(*, session: Session = Depends(_services.get_session), member_id: int):
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
    db_hall = _models.Hall.from_orm(hall)
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


@app.post("/api/committees/", tags=["committees"], response_model=_schemas.InfoCreate)
def create_committee(*, session: Session = Depends(_services.get_session), committee: _schemas.InfoCreate):
    db_committee = _models.Committee.from_orm(committee)
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


@app.get("/api/committees/{committee_id}",  tags=["committees"], response_model=_schemas.InfoRead)
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
    db_event = _models.Event.from_orm(event)
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
    if attendee in event.members_attended:
        raise HTTPException(status_code=404, detail="Member already attended")
    event.members_attended.append(attendee)
    session.add(event)
    session.commit()
    return ({"ok": True})


@app.post("/api/categories/", tags=["categories"], response_model=_schemas.InfoCreate)
def create_category(*, session: Session = Depends(_services.get_session), category: _schemas.InfoCreate):
    db_category = _models.Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@ app.get("/api/categories/",  tags=["categories"], response_model=List[_schemas.InfoRead])
def read_categories(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    categories = session.exec(
        select(_models.Category).offset(offset).limit(limit)).all()
    return categories


@app.get("/api/categories/{category_id}",  tags=["categories"], response_model=_schemas.InfoRead)
def read_category(*, session: Session = Depends(_services.get_session), category_id: int):
    category = session.get(_models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.patch("/api/categories/{category_id}",  tags=["categories"], response_model=_schemas.InfoRead)
def update_category(
    *, session: Session = Depends(_services.get_session), category_id: int, category: _schemas.InfoUpdate
):
    db_category = session.get(_models.Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.delete("/api/categories/{categoty_id}",  tags=["categories"])
def delete_category(*, session: Session = Depends(_services.get_session), category_id: int):

    category = session.get(_models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}


@app.post("/api/semesters/", tags=["semesters"], response_model=_schemas.InfoCreate)
def create_semester(*, session: Session = Depends(_services.get_session), semester: _schemas.InfoCreate):
    db_semester = _models.Semester.from_orm(semester)
    session.add(db_semester)
    session.commit()
    session.refresh(db_semester)
    return db_semester


@ app.get("/api/semesters/",  tags=["semesters"], response_model=List[_schemas.InfoRead])
def read_semesters(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    semesters = session.exec(
        select(_models.Semester).offset(offset).limit(limit)).all()
    return semesters


@app.get("/api/semesters/{semester_id}",  tags=["semesters"], response_model=_schemas.InfoRead)
def read_semester(*, session: Session = Depends(_services.get_session), semester_id: int):
    semester = session.get(_models.Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@app.patch("/api/semesters/{semester_id}",  tags=["semesters"], response_model=_schemas.InfoRead)
def update_semester(
    *, session: Session = Depends(_services.get_session), semester_id: int, semester: _schemas.InfoUpdate
):
    db_semester = session.get(_models.Semester, semester_id)
    if not db_semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    semester_data = semester.dict(exclude_unset=True)
    for key, value in semester_data.items():
        setattr(db_semester, key, value)
    session.add(db_semester)
    session.commit()
    session.refresh(db_semester)
    return db_semester


@app.delete("/api/semesters/{semester_id}",  tags=["semesters"])
def delete_semester(*, session: Session = Depends(_services.get_session), semester_id: int):

    semester = session.get(_models.Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    session.delete(semester)
    session.commit()
    return {"ok": True}
