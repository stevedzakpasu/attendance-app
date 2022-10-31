from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Hall(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Programme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Level(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Congregation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Committee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class MemberEventLink(SQLModel, table=True):
    event_id: Optional[int] = Field(
        default=None, foreign_key="event.id", primary_key=True
    )
    member_id: Optional[int] = Field(
        default=None, foreign_key="member.id", primary_key=True
    )


class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone_number: str
    hall: Optional[str] = Field(default=None, foreign_key="hall.name")
    room_number: Optional[str]
    programme: Optional[str] = Field(
        default=None, foreign_key="programme.name")
    level: Optional[str] = Field(default=None, foreign_key="level.name")
    DOB: str
    congregation: str = Field(
        default=None, foreign_key="congregation.name")
    committee: Optional[str] = Field(
        default=None, foreign_key="committee.name")
    events_attended: List["Event"] = Relationship(
        back_populates="members_attended", link_model=MemberEventLink)


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    members_attended: List["Member"] = Relationship(
        back_populates="events_attended", link_model=MemberEventLink)
