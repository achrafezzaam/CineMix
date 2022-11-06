from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies_table"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    desc = Column(String, index=True)

class Room(Base):
    __tablename__ = "rooms_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rows = Column(Integer, index=True)
    cols = Column(Integer, index=True)

class Seat(Base):
    __tablename__ = "seats_table"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms_table.id"))
    room = relationship("Room")
    row = Column(Integer, index=True)
    col = Column(Integer, index=True)

class Session(Base):
    __tablename__ = "sessions_table"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies_table.id"))
    movie = relationship("Movie")
    time = Column(Time)

class Ticket(Base):
    __tablename__ = "tickets_table"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies_table.id"))
    movie = relationship("Movie", foreign_keys=[movie_id])
    seat_id = Column(Integer, ForeignKey("seats_table.id"))
    seat = relationship("Seat", foreign_keys=[seat_id])
    session_id = Column(Integer, ForeignKey("sessions_table.id"))
    session = relationship("Session", foreign_keys=[session_id])
    printed_at = Column(Time, default=datetime.now().time())