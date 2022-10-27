from models import Movie, Room, Seat, Session

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.CineMix
collection = database.cinema

# Movies functions

async def fetch_all_movies():
    movies = []
    cursor = collection.find({})
    async for document in cursor:
        movies.append(Movie(**document))
    return movies

async def fetch_one_movie(title):
    document = await collection.find_one({"title":title})
    return document

async def create_movie(movie):
    document = movie
    result = await collection.insert_one(document)
    return document

async def update_movie(title, desc):
    await collection.update_one({"title":title}, {"$set":{"description":desc}})
    document = await collection.find_one({"title":title})
    return document

async def remove_movie(title):
    await collection.delete_one({"title":title})
    return True

# Rooms functions

async def fetch_all_rooms():
    rooms = []
    cursor = collection.find({})
    async for document in cursor:
        rooms.append(Room(**document))
    return rooms

async def fetch_one_room(id):
    document = await collection.find_one({"id":id})
    return document

async def create_room(room):
    document = room
    result = await collection.insert_one(room)
    return document

async def update_room(id, movie):
    await collection.update_one({"id":id}, {"$set":{"movie":movie}})
    document = await collection.find_one({"id":id})
    return document

async def remove_room(id):
    await collection.delete_one({"id":id})
    return True

# Seats functions

async def fetch_all_seats(room):
    seats = []
    cursor = collection.find({"room":room})
    async for document in cursor:
        seats.append(Seat(**document))
    return seats

async def fetch_one_seat(room, row, col):
    document = await collection.find_one({"id":id, "row":row, "col":col})
    return document

# Sessions functions

async def fetch_all_sessions(movie):
    sessions = []
    cursor = collection.find({"movie":movie})
    async for document in cursor:
        sessions.append(Session(**document))
    return sessions

async def fetch_one_session(movie,time):
    document = await collection.find_one({"movie":movie, "time":time})
    return document