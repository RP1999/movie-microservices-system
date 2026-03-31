import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB connection URI from environment with Atlas fallback
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:admin123@cluster0.ncxtapi.mongodb.net/movie_system")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Ping database to confirm connection
    client.admin.command('ping')
    db = client["movie_system"]
    print(f"SUCCESS: Connected to Review MongoDB: {MONGO_URI[:30]}...")
except Exception as e:
    db = None
    print(f"ERROR: Failed to connect to Review MongoDB: {e}")

review_collection = db["comments"] if db is not None else None
