from typing import List, Optional
from sqlmodel import SQLModel
import datetime


class MemberCreate(SQLModel):
    first_name: str
    other_names: Optional[str]
    last_name: str
    sex: str
    phone_number: str
    hall: Optional[str]
    room_number: Optional[str]
    programme: Optional[str]
    level: Optional[str]
    date_of_birth: datetime.date
    congregation: str
    committee: Optional[str]


class MemberUpdate(SQLModel):
    first_name: Optional[str] = None
    other_names: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[str] = None
    phone_number: Optional[str] = None
    hall: Optional[str] = None
    room_number: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    congregation: Optional[str] = None
    committee: Optional[str] = None


class EventCreate(SQLModel):
    name: str
    category: str
    semester: str


class EventRead(EventCreate):
    id: int
    created_on: datetime.date


class EventUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    semester: Optional[str] = None


class MemberRead(MemberCreate):
    id: int


class MemberReadWithEvents(MemberRead):
    events_attended: List[EventRead] = []


class EventReadWithMembers(EventRead):
    members_attended: List[MemberRead] = []


class InfoCreate(SQLModel):
    name: str


class InfoRead(InfoCreate):
    id: int


class InfoUpdate(SQLModel):
    name: Optional[str] = None
