import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Id:
    id: uuid


@dataclass
class Time(Id):
    updated_at: datetime
    created_at: datetime


@dataclass
class Movie(Time):
    title: str
    rating: Optional[float]
    type: str
    description: Optional[str]
    file_path: Optional[str]
    creation_date: datetime = field(default_factory=datetime.now)


@dataclass
class Genre(Time):
    name: str
    description: Optional[str] = None


@dataclass
class GenreFilmwork(Id):
    film_work_id: uuid = field(default_factory=uuid.uuid4)
    genre_id: uuid = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Person(Time):
    full_name: str


@dataclass
class PersonFilmwork(Id):
    role: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    film_work_id: uuid = field(default_factory=uuid.uuid4)
    person_id: uuid = field(default_factory=uuid.uuid4)


TABLES = {
    'film_work': Movie,
    'genre': Genre,
    'genre_film_work': GenreFilmwork,
    'person': Person,
    'person_film_work': PersonFilmwork,
}
