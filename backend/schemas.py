from datetime import time
from typing import Optional
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
    time        : time

    class Config:
        orm_mode = True

class Ticket(BaseModel):
    id          : Optional[int]
    movie_id    : int
    seat_id     : int
    session_id  : int
    printed_at  : time

    class Config:
        orm_mode = True