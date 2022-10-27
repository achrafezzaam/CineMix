from typing import Tuple
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Movie, Room, Seat, Session

app = FastAPI()

from database import (
    fetch_all_movies,
    fetch_one_movie,
    create_movie,
    update_movie,
    remove_movie,

    fetch_all_rooms,
    fetch_one_room,
    create_room,
    update_room,
    remove_room,

    fetch_all_seats,
    fetch_one_seat,

    fetch_all_sessions,
    fetch_one_session,
)

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
    return 'Welcome to the root page'

# Movie api views

@app.get('/api/movie')
async def get_movies():
    response = await fetch_all_movies()
    return response

@app.get('/api/movie/{title}', response_model=Movie)
async def get_movie_by_title(title):
    response = await fetch_one_movie(title)
    if response:
        return response
    raise HTTPException(404, f"Movie with the title {title} was not found")

@app.post('/api/movie', response_model=Movie)
async def post_movie(movie:Movie):
    response = await create_movie(movie.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put('/api/movie/{title}', response_model=Movie)
async def put_movie(title: str, desc: str):
    response = await update_movie(title, desc)
    if response:
        return response
    raise HTTPException(404, f"The movie with title {title} wasn't found")

@app.delete('/api/movie/{title}')
async def delete_movie(title):
    response = remove_movie(title)
    if response:
        return "Movie deleted successfully"
    raise HTTPException(400, "Something went wrong")

# Room api views

@app.get('/api/room')
async def get_rooms():
    response = await fetch_all_rooms()
    return response

@app.get('/api/room/{id}', response_model=Room)
async def get_room_by_id(id):
    response = await fetch_one_room(id)
    if response:
        return response
    raise HTTPException(404, f"The room with the id {id} doesn't exist")

@app.post('/api/room', response_model=Room)
async def post_room(room:Room):
    response = await create_room(room.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put('/api/room/{id}', response_model=Room)
async def put_room(id: str, movie: str):
    response = await update_room(id,movie)
    if response:
        return response
    raise HTTPException(404, f"The room with the id {id} deosn't exist")

@app.delete('/api/room/{id}')
async def delete_room(id):
    response = await remove_room(id)
    if response:
        return "The room was deleted successfully"
    raise HTTPException(400, "Something went wrong")

# Seat api views

@app.get('/api/seat/{room}', response_model=Seat)
async def get_seats_by_room(room):
    response = await fetch_all_seats(room)
    if response:
        return response
    raise HTTPException(404, f"This room deosn't exist")

@app.get('/api/seat/{room}{row}{col}', response_model=Seat)
async def get_seat(room, row, col):
    response = await fetch_one_seat(room, row, col)
    if response:
        return response
    raise HTTPException(404, "This seat doesn't exist")

# Session api views

@app.get('/api/session/{movie}', response_model=Session)
async def get_sessions_by_movie(movie):
    response = fetch_all_sessions(movie)
    if response:
        return response
    raise HTTPException(404, f"This Movie doesn't exist")

@app.get('/api/session/{movie}', response_model=Session)
async def get_session(movie, time:Tuple[int,int]):
    response = await fetch_one_session(movie,time)
    if response:
        return response
    raise HTTPException(404, "This movie session deosn't exist")