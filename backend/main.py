from typing import Tuple, List
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models
from schemas import Movie, Room, Seat, Session, Ticket
from database import SessionLocal, engine
from datetime import time

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

@app.get('/')
async def index():
    return RedirectResponse(url='/docs/')

# Movie api views

@app.get('/api/movie', response_model=List[Movie])
async def get_movies(db: Session = Depends(get_db)):
    response = db.query(models.Movie).all()
    return response

@app.get('/api/movie/{title}', response_model=Movie)
async def get_movie_by_title(title:str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter_by(title=title).first()
    return movie

@app.post('/api/movie')
async def post_movie(title:str, desc:str, db: Session = Depends(get_db)):
    movie = models.Movie(title=title,desc=desc)
    db.add(movie)
    db.commit()
    return "Movie created successfully"

@app.put('/api/movie/{title}')
async def put_movie(id: int, title: str, desc: str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).get(id)
    movie.title = title
    movie.desc = desc
    db.add(movie)
    db.commit()
    return "The Movie's data was updated successfully"

@app.delete('/api/movie/{id}')
async def delete_movie(id, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).get(id)
    row_deleted = db.delete(movie)
    db.commit()
    return "Movie deleted successfully"

# # Room api views

@app.get('/api/room', response_model=List[Room])
async def get_rooms(db: Session = Depends(get_db)):
    response = db.query(models.Room).all()
    return response

@app.get('/api/room/{id}', response_model=Room)
async def get_room_by_id(id, db: Session = Depends(get_db)):
    room = db.query(models.Room).get(id)
    return room

@app.post('/api/room')
async def post_room(name:str, rows:int, cols:int, db: Session = Depends(get_db)):
    room = models.Room(name=name,rows=rows,cols=cols)
    db.add(room)
    db.commit()
    for row in range(rows):
        for col in range(cols):
            seat = models.Seat(room_id=room.id,col=(col+1),row=(row+1))
            db.add(seat)
            db.commit()
    return f"The room {name} was created successfully"

@app.put('/api/room/{id}', response_model=Room)
async def put_room(id:int, name:str, cols:int, rows:int, db: Session = Depends(get_db)):
    room = db.query(models.Room).get(id)
    room.name = name
    room.cols = cols
    room.rows = rows
    db.add(room)
    db.commit()
    return "The Room's data was updated successfully"

@app.delete('/api/room/{id}')
async def delete_room(id, db: Session = Depends(get_db)):
    room = db.query(models.Room).get(id)
    row_deleted = db.delete(room)
    seats_deleted = db.query(models.Seat).filter_by(room_id=id).delete()
    db.commit()
    return "Room deleted successfully"

# # Seat api views

@app.get('/api/seats/{room}', response_model=List[Seat])
async def get_seats_by_room(room_id, db: Session = Depends(get_db)):
    seats_list = db.query(models.Seat).filter_by(room_id=room_id).all()
    return seats_list

@app.get('/api/seat/{room}', response_model=Seat)
async def get_seat(room_id:int, row:int, col:int, db: Session = Depends(get_db)):
    seat = db.query(models.Seat).filter_by(room_id=room_id,row=row,col=col).first()
    return seat

# # Session api views

@app.get('/api/sessions', response_model=List[Session])
async def get_sessions(db: Session = Depends(get_db)):
    movie_sessions = db.query(models.Session).all()
    return movie_sessions

@app.get('/api/sessions/{movie}', response_model=List[Session])
async def get_sessions_by_movie(movie:str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter_by(title=movie).first()
    movie_sessions = db.query(models.Session).filter_by(movie_id=movie.id).all()
    return movie_sessions

@app.post('/api/session/')
async def post_session(movie_id:int, time:time, db: Session = Depends(get_db)):
    movie_session = models.Session(movie_id=movie_id,time=time)
    db.add(movie_session)
    db.commit()
    return "Session created successfully"
# @app.get('/api/session/{movie}', response_model=Session)
# async def get_session(movie, time:Tuple[int,int]):
#     response = await fetch_one_session(movie,time)
#     if response:
#         return response
#     raise HTTPException(404, "This movie session deosn't exist")

# # Ticket api views
@app.get('/api/ticket/{id}', response_model=Ticket)
async def get_ticket_by_id(id:int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).get(id)
    return ticket

@app.post('/api/ticket/')
async def post_ticket(movie_id:int, seat_id:int, session_id:int, db: Session = Depends(get_db)):
    ticket = models.Ticket(movie_id=movie_id,seat_id=seat_id, session_id=session_id)
    db.add(ticket)
    db.commit()
    return "The ticket was created successfully"