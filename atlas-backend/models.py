from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field, Column, JSON


class LocationType(str, Enum):
    city = "city"
    residence = "residence"
    prison = "prison"
    port = "port"
    waypoint = "waypoint"
    site = "site"


class Location(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    type: LocationType
    coords: List[float] = Field(sa_column=Column(JSON))
    description: Optional[str] = None


class Person(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    role: Optional[str] = None


class Writing(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    locId: Optional[str] = Field(default=None, foreign_key="location.id")
    year: Optional[int] = None


class EventType(str, Enum):
    birth = "birth"
    death = "death"
    journey = "journey"
    residence = "residence"
    exile = "exile"
    imprisonment = "imprisonment"
    declaration = "declaration"
    battle = "battle"
    publication = "publication"
    other = "other"


class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    type: EventType
    dateStart: str
    dateEnd: Optional[str] = None
    locId: Optional[str] = Field(default=None, foreign_key="location.id")
    journeyPath: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    peopleIds: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    writingIds: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    source: Optional[str] = None


class AtlasDB(BaseModel):
    locations: List[Location] = PydanticField(default_factory=list)
    people: List[Person] = PydanticField(default_factory=list)
    writings: List[Writing] = PydanticField(default_factory=list)
    events: List[Event] = PydanticField(default_factory=list)
