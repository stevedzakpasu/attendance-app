from fastapi import FastAPI, Depends, Query, HTTPException
from typing import List
import services as _services
import models as _models
from sqlmodel import Session, select
import schemas as _schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Request
import time
from fastapi.middleware.cors import CORSMiddleware
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
        "name": "events categories",
        "description": "Operations with **events categories**",
    },
    {
        "name": "semesters",
        "description": "Operations with **semesters**",
    },    {
        "name": "users",
        "description": "Operations with **users**",
    },
]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(openapi_tags=tags_metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SECRET_KEY = "a924c4a7c5e0019a69c15412b4f01dd451023fce957a606223ed390fdba1a809"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# @app.on_event("startup")
# def on_startup():
#     _services.create_admin()


@app.post("/api/members/", tags=["members"], response_model=_schemas.MemberCreate, dependencies=[Depends(_services.get_current_user)])
def create_member(*, session: Session = Depends(_services.get_session), member: _schemas.MemberCreate, user: _models.User = Depends(_services.get_current_user)):
    db_member = _models.Member.from_orm(member)
    db_user = session.get(_models.User, user.username)
    if not db_user.is_admin:
        db_user.member = db_member
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@ app.get("/api/members/",  tags=["members"], response_model=List[_schemas.MemberReadWithEvents], dependencies=[Depends(_services.get_current_admin_user)])
def read_members(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=1000, lte=1000)
):
    members = session.exec(
        select(_models.Member).offset(offset).limit(limit)).all()
    return members


@ app.get("/api/members_cards/",  tags=["members"], response_model=List[_schemas.MemberRead],  dependencies=[Depends(_services.get_current_admin_user)])
def read_members(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=1000, lte=1000)
):
    members = session.exec(
        select(_models.Member).offset(offset).limit(limit)).all()
    return members


@app.get("/api/members/{member_id}",  tags=["members"], response_model=_schemas.MemberReadWithEvents, dependencies=[Depends(_services.get_current_user)])
def read_member(*, session: Session = Depends(_services.get_session), member_id: int, user: _models.User = Depends(_services.get_current_user)):
    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_user = session.get(_models.User, user.username)
    if member.id != db_user.member_id and not db_user.is_admin:
        raise HTTPException(
            status_code=400, detail="You don't have rights to perform this operation")
    return member


@app.get("/api/members_cards/{member_id}",  tags=["members"], response_model=_schemas.MemberRead, dependencies=[Depends(_services.get_current_user)])
def read_member_without_events(*, session: Session = Depends(_services.get_session), member_id: int, user: _models.User = Depends(_services.get_current_user)):
    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_user = session.get(_models.User, user.username)
    if member.id != db_user.member_id and not db_user.is_admin:
        raise HTTPException(
            status_code=400, detail="You don't have rights to perform this operation")
    return member


@app.patch("/api/members/{member_id}",  tags=["members"], response_model=_schemas.MemberReadWithEvents, dependencies=[Depends(_services.get_current_user)])
def update_member(
    *, session: Session = Depends(_services.get_session), member_id: int, member: _schemas.MemberUpdate, user: _models.User = Depends(_services.get_current_user)
):
    db_member = session.get(_models.Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    member_data = member.dict(exclude_unset=True)
    db_user = session.get(_models.User, user.username)
    if db_member.id != db_user.member_id and not db_user.is_admin:
        raise HTTPException(
            status_code=400, detail="You don't have rights to perform this operation")
    for key, value in member_data.items():
        setattr(db_member, key, value)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@app.delete("/api/members/{member_id}",  tags=["members"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_member(*, session: Session = Depends(_services.get_session), member_id: int,  user: _models.User = Depends(_services.get_current_user)):

    member = session.get(_models.Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    session.delete(member)
    session.commit()
    return {"message": "Member successfully deleted"}


@app.post("/api/halls/", tags=["halls"], response_model=_schemas.InfoCreate, dependencies=[Depends(_services.get_current_admin_user)])
def create_hall(*, session: Session = Depends(_services.get_session), hall: _schemas.InfoCreate):
    db_hall = _models.Hall.from_orm(hall)
    session.add(db_hall)
    session.commit()
    session.refresh(db_hall)
    return db_hall


@ app.get("/api/halls/",  tags=["halls"], response_model=List[_schemas.InfoRead], dependencies=[Depends(_services.get_current_user)])
def read_halls(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    halls = session.exec(
        select(_models.Hall).offset(offset).limit(limit)).all()
    return halls


@app.get("/api/halls/{hall_id}",  tags=["halls"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
def read_hall(*, session: Session = Depends(_services.get_session), hall_id: int):
    hall = session.get(_models.Hall, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall


@app.patch("/api/halls/{hall_id}",  tags=["halls"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
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


@app.delete("/api/halls/{hall_id}",  tags=["halls"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_hall(*, session: Session = Depends(_services.get_session), hall_id: int):

    hall = session.get(_models.Hall, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    session.delete(hall)
    session.commit()
    return {"message": "Hall successfully deleted"}


@app.post("/api/committees/", tags=["committees"], response_model=_schemas.InfoCreate,  dependencies=[Depends(_services.get_current_admin_user)])
def create_committee(*, session: Session = Depends(_services.get_session), committee: _schemas.InfoCreate):
    db_committee = _models.Committee.from_orm(committee)
    session.add(db_committee)
    session.commit()
    session.refresh(db_committee)
    return db_committee


@ app.get("/api/committees/",  tags=["committees"], response_model=List[_schemas.InfoRead], dependencies=[Depends(_services.get_current_user)])
def read_committee(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    committees = session.exec(
        select(_models.Committee).offset(offset).limit(limit)).all()
    return committees


@app.get("/api/committees/{committee_id}",  tags=["committees"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
def read_committees(*, session: Session = Depends(_services.get_session), committee_id: int):
    committee = session.get(_models.Congregation, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    return committee


@app.patch("/api/committees/{committee_id}",  tags=["committees"], response_model=_schemas.InfoRead,  dependencies=[Depends(_services.get_current_admin_user)])
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


@app.delete("/api/committees/{committee_id}",  tags=["committees"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_committee(*, session: Session = Depends(_services.get_session), committee_id: int, ):

    committee = session.get(_models.Committee, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    session.delete(committee)
    session.commit()
    return {"message": "Committee successfully deleted"}


@app.post("/api/events/", tags=["events"], response_model=_schemas.EventCreate, dependencies=[Depends(_services.get_current_admin_user)])
def create_event(*, session: Session = Depends(_services.get_session), event: _schemas.EventCreate):
    db_event = _models.Event.from_orm(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@ app.get("/api/events/",  tags=["events"], response_model=List[_schemas.EventReadWithMembers], dependencies=[Depends(_services.get_current_admin_user)])
def read_event(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    events = session.exec(
        select(_models.Event).offset(offset).limit(limit)).all()
    return events


@app.get("/api/events/{event_id}",  tags=["events"], response_model=_schemas.EventReadWithMembers, dependencies=[Depends(_services.get_current_admin_user)])
def read_events(*, session: Session = Depends(_services.get_session), event_id: int):
    event = session.get(_models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.patch("/api/events/{event_id}",  tags=["events"], response_model=_schemas.EventReadWithMembers, dependencies=[Depends(_services.get_current_admin_user)])
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


@app.delete("/api/events/{event_id}",  tags=["events"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_event(*, session: Session = Depends(_services.get_session), event_id: int, token: str = Depends(oauth2_scheme)):

    event = session.get(_models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return {"message": "Event successfully deleted"}


@app.post("/api/events/{event_id}/add_attendee",  tags=["events"], dependencies=[Depends(_services.get_current_admin_user)])
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
    return {"message": "Member successfully marked present"}


@app.post("/api/categories/", tags=["events categories"], response_model=_schemas.InfoCreate, dependencies=[Depends(_services.get_current_admin_user)])
def create_category(*, session: Session = Depends(_services.get_session), category: _schemas.InfoCreate):
    db_category = _models.Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@ app.get("/api/categories/",  tags=["events categories"], response_model=List[_schemas.InfoRead], dependencies=[Depends(_services.get_current_user)])
def read_categories(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    categories = session.exec(
        select(_models.Category).offset(offset).limit(limit)).all()
    return categories


@app.get("/api/categories/{category_id}",  tags=["events categories"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
def read_category(*, session: Session = Depends(_services.get_session), category_id: int):
    category = session.get(_models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.patch("/api/categories/{category_id}",  tags=["events categories"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
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


@app.delete("/api/categories/{categoty_id}",  tags=["events categories"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_category(*, session: Session = Depends(_services.get_session), category_id: int):

    category = session.get(_models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}


@app.post("/api/semesters/", tags=["semesters"], response_model=_schemas.InfoCreate, dependencies=[Depends(_services.get_current_admin_user)])
def create_semester(*, session: Session = Depends(_services.get_session), semester: _schemas.InfoCreate):
    db_semester = _models.Semester.from_orm(semester)
    session.add(db_semester)
    session.commit()
    session.refresh(db_semester)
    return db_semester


@ app.get("/api/semesters/",  tags=["semesters"], response_model=List[_schemas.InfoRead], dependencies=[Depends(_services.get_current_admin_user)])
def read_semesters(
    *,
    session: Session = Depends(_services.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
):
    semesters = session.exec(
        select(_models.Semester).offset(offset).limit(limit)).all()
    return semesters


@app.get("/api/semesters/{semester_id}",  tags=["semesters"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
def read_semester(*, session: Session = Depends(_services.get_session), semester_id: int, token: str = Depends(oauth2_scheme)):
    semester = session.get(_models.Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester


@app.patch("/api/semesters/{semester_id}",  tags=["semesters"], response_model=_schemas.InfoRead, dependencies=[Depends(_services.get_current_admin_user)])
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


@app.delete("/api/semesters/{semester_id}",  tags=["semesters"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_semester(*, session: Session = Depends(_services.get_session), semester_id: int):

    semester = session.get(_models.Semester, semester_id)
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    session.delete(semester)
    session.commit()
    return {"message": "Semester successfully deleted"}


@app.post("/token", response_model=_schemas.Token, tags=["users"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = _services.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=_schemas.UserOutSchema, tags=["users"])
def create_new_user(userIn: _schemas.UserInSchema, session: Session = Depends(_services.get_session)):

    user = session.get(_models.User, userIn.username)
    if user:
        raise HTTPException(
            status_code=409,
            detail="Username and/or e-mail already exists",
        )

    new_user = _models.User(
        username=userIn.username,
        email=userIn.email,
        full_name=userIn.full_name,
        hashed_password=_services.get_password_hash(userIn.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get("/users/me/",  tags=["users"], response_model=_schemas.UserOutSchema, dependencies=[Depends(_services.get_current_active_user)])
async def read_users_me(current_user: _models.User = Depends(_services.get_current_active_user), session: Session = Depends(_services.get_session)):

    user = session.get(_models.User, current_user.username)
    return user


@app.get("/users/all/",  tags=["users"], response_model=List[_schemas.UserOutSchema], dependencies=[Depends(_services.get_current_admin_user)])
async def read_all_users(session: Session = Depends(_services.get_session),  offset: int = 0,
                         limit: int = Query(default=1000, lte=1000)):
    users = session.exec(
        select(_models.User).offset(offset).limit(limit)).all()
    return users


@app.post("/api/users/{username}", tags=["users"], dependencies=[Depends(_services.get_current_admin_user)])
def reset_password(*, session: Session = Depends(_services.get_session), username: str, password: str):
    user = session.get(_models.User, username)
    db_user = session.exec(
        select(_models.User).where(_models.User.username == user.username)
    ).one()
    db_user.hashed_password = _services.get_password_hash(password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "Password successfully reset"}


@app.delete("/api/users/{username}",  tags=["users"], dependencies=[Depends(_services.get_current_admin_user)])
def delete_user(*, session: Session = Depends(_services.get_session), username: str):

    user = session.get(_models.User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User successfully deleted"}
