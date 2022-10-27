from pydantic import BaseModel

class Movie(BaseModel):
    title   : str
    desc    : str

class Room(BaseModel):
    id      : str
    movie   : str

class Seat(BaseModel):
    room    : str
    row     : str
    col     : str