import motor.motor_asyncio
import os

MONGO_DETAILS = "mongodb+srv://admin:admin123@cluster0.ncxtapi.mongodb.net/movie_system"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.movie_system
movies_collection = database.get_collection("movies_analytics")
