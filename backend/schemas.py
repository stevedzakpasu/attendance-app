from typing import List, Optional
from sqlmodel import SQLModel


class MemberCreate(SQLModel):
    name: str
    phone_number: str
    hall: Optional[str]
    room_number: Optional[str]
    programme: Optional[str]
    level: Optional[str]
    DOB: str
    congregation: str
    committee: Optional[str]


class MemberUpdate(SQLModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    hall: Optional[str] = None
    room_number: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    DOB: Optional[str] = None
    congregation: Optional[str] = None
    committee: Optional[str] = None


class EventCreate(SQLModel):
    name: str


class EventRead(EventCreate):
    id: int


class EventUpdate(SQLModel):
    name: Optional[str] = None


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
