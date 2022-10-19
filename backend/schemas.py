from typing import Optional
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


class MemberRead(MemberCreate):
    id: int


class EventCreate(SQLModel):
    name: str


class EventRead(EventCreate):
    id: int


class HallCreate(SQLModel):
    name: str


class HallRead(HallCreate):
    id: int


class ProgrammeCreate(SQLModel):
    name: str


class ProgrammeRead(ProgrammeCreate):
    id: int


class LevelCreate(SQLModel):
    name: str


class LevelRead(LevelCreate):
    id: int


class CongregationCreate(SQLModel):
    name: str


class CongregationRead(CongregationCreate):
    id: int


class CommitteeCreate(SQLModel):
    name: str


class CommitteeRead(CommitteeCreate):
    id: int
