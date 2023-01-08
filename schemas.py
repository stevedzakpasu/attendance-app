from typing import List, Optional
from sqlmodel import SQLModel
import datetime
from pydantic import EmailStr


class MemberCreate(SQLModel):
    first_name: str
    other_names: Optional[str]
    last_name: str
    sex: str
    date_of_birth: datetime.date
    phone_number: str
    hall: Optional[str]
    room_number: Optional[str]
    programme: Optional[str]
    level: Optional[str]
    congregation: str
    committee_1: Optional[str]
    committee_2: Optional[str]
    committee_3: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_relationship: Optional[str]
    emergency_contact_phone_number: Optional[str]


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
    committee_1: Optional[str] = None
    committee_2: Optional[str] = None
    committee_3: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    emergency_contact_phone_number: Optional[str] = None


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


class User(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class UserOutSchema(SQLModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool
    is_admin: bool
    member_id: int | None
    member: MemberRead | None


class UserInSchema(SQLModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
