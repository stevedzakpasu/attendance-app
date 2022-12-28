from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
import datetime
from sqlalchemy import Column, String


class Hall(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))


class Semester(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))


class Committee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))


class MemberEventLink(SQLModel, table=True):
    event_id: Optional[int] = Field(
        default=None, foreign_key="event.id", primary_key=True
    )
    member_id: Optional[int] = Field(
        default=None, foreign_key="member.id", primary_key=True
    )


class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    other_names: Optional[str]
    last_name: str
    sex: str
    phone_number: str
    hall: Optional[str] = Field(default=None, foreign_key="hall.name")
    room_number: Optional[str]
    programme: Optional[str]
    level: Optional[str]
    date_of_birth: datetime.date
    congregation: Optional[str]
    committee: Optional[str] = Field(
        default=None, foreign_key="committee.name")
    events_attended: List["Event"] = Relationship(
        back_populates="members_attended", link_model=MemberEventLink)
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="member"
    )


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    members_attended: List["Member"] = Relationship(
        back_populates="events_attended", link_model=MemberEventLink)
    semester: str = Field(
        default=None, foreign_key="semester.name")
    category: str = Field(
        default=None, foreign_key="category.name")
    created_on: datetime.date = Field(
        default_factory=datetime.date.today, nullable=False)


class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True, index=True,
                          nullable=False,)
    email: EmailStr
    full_name: Optional[str] = ""
    hashed_password: Optional[str] = ""
    disabled: Optional[bool] = False
    is_admin: Optional[bool] = False
    member_id: Optional[int] = Field(
        default=None, foreign_key="member.id")
    member: Optional["Member"] = Relationship(
        back_populates="user")
