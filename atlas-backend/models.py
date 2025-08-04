from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    id: str
    name: str
    type: Literal["city", "residence", "prison", "port", "waypoint", "site"]
    coords: tuple[float, float]
    description: Optional[str] = None


class Person(BaseModel):
    id: str
    name: str
    role: Optional[str] = None


class Writing(BaseModel):
    id: str
    name: str
    locId: Optional[str] = None
    year: Optional[int] = None


class Event(BaseModel):
    id: str
    name: str
    type: Literal[
        "birth",
        "death",
        "journey",
        "residence",
        "exile",
        "imprisonment",
        "declaration",
        "battle",
        "publication",
        "other",
    ]
    dateStart: str
    dateEnd: Optional[str] = None
    locId: Optional[str] = None
    journeyPath: Optional[List[str]] = None
    peopleIds: Optional[List[str]] = None
    writingIds: Optional[List[str]] = None
    source: Optional[str] = None


class AtlasDB(BaseModel):
    locations: List[Location] = Field(default_factory=list)
    people: List[Person] = Field(default_factory=list)
    writings: List[Writing] = Field(default_factory=list)
    events: List[Event] = Field(default_factory=list)
