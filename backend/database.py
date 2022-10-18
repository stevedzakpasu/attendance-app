from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, create_engine


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
    room_number: str
    programme: Optional[str] = Field(
        default=None, foreign_key="programme.name")
    level: Optional[str] = Field(default=None, foreign_key="level.name")
    DOB: str
    congregation: Optional[str] = Field(
        default=None, foreign_key="congregation.name")
    committee: Optional[str] = Field(
        default=None, foreign_key="committee.name")
    events_attended: List["Event"] = Relationship(
        back_populates="members", link_model=MemberEventLink)


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: datetime
    member_attended: List["Member"] = Relationship(
        back_populates="events", link_model=MemberEventLink)


engine = create_engine("sqlite:///database.db")


if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)
