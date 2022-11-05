from typing import Tuple, Optional
from pydantic import BaseModel

class Movie(BaseModel):
    id      : Optional[int]
    title   : str
    desc    : str

    class Config:
        orm_mode = True

class Room(BaseModel):
    id     : Optional[int]
    name   : str
    rows   : int
    cols   : int

    class Config:
        orm_mode = True

class Seat(BaseModel):
    id      : Optional[int]
    room_id : int
    row     : int
    col     : int

    class Config:
        orm_mode = True

class Session(BaseModel):
    id          : Optional[int]
    movie_id    : int
    time        : Tuple[int, int]

    class Config:
        orm_mode = True