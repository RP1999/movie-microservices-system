from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os

from schemas import StreamResponse, WatchRequest, WatchRecord, WatchProgressRequest

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Streaming Service",
    description="Microservice responsible for managing movie streams and watch history.",
    version="1.0.0"
)

# Database Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.server_info() # Trigger exception if cannot connect to db
    db = client["movie_system"]
    watch_collection = db["watch_history"]
    db_status = "Connected"
except Exception as e:
    db_status = "Disconnected"
    watch_collection = None
    print(f"Failed to connect to MongoDB: {e}")

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint to ensure the service is running."""
    return {"service": "Streaming", "status": "Running", "db": db_status}

@app.get("/stream/{movie_id}", response_model=StreamResponse, tags=["Streaming"])
def stream_movie(movie_id: str):
    """
    Get the streaming URL for a specific movie.
    In a real system, this would fetch signed URLs from S3 or a CDN.
    """
    if not movie_id:
        raise HTTPException(status_code=400, detail="Movie ID is required")
        
    return StreamResponse(
        movie_id=movie_id,
        stream_url=f"http://localhost:8003/play/{movie_id}",
        quality="1080p",
        status="ready"
    )

@app.post("/watch", status_code=status.HTTP_201_CREATED, tags=["Watch History"])
def save_watch(watch_request: WatchRequest):
    """
    Record that a user started watching a movie.
    """
    if watch_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    record = {
        "user_id": watch_request.user_id,
        "movie_id": watch_request.movie_id,
        "time": datetime.now()
    }
    
    watch_collection.insert_one(record)
    return {"message": "Watch history saved successfully"}

@app.get("/watch/{user_id}", response_model=List[WatchRecord], tags=["Watch History"])
def get_watch_history(user_id: str):
    """
    Retrieve the entire watch history for a specific user.
    """
    if watch_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    data = list(watch_collection.find({"user_id": user_id}, {"_id": 0}))
    return data

@app.put("/watch/progress", tags=["Watch History"])
def update_progress(progress_request: WatchProgressRequest):
    """
    Save the user's progress for a movie they are watching.
    """
    if watch_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    result = watch_collection.update_one(
        {"user_id": progress_request.user_id, "movie_id": progress_request.movie_id},
        {"$set": {"progress_minutes": progress_request.progress_minutes, "status": "paused", "time": datetime.now()}},
        upsert=True
    )
    
    return {"message": "Watch progress saved successfully"}

@app.delete("/watch/{user_id}", tags=["Watch History"])
def clear_history(user_id: str):
    """
    Clear all watch history for a specific user.
    """
    if watch_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    result = watch_collection.delete_many({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No watch history found to delete")
        
    return {"message": f"Successfully deleted {result.deleted_count} watch records"}
@app.delete("/watch/{user_id}/{movie_id}", tags=["Watch History"])
def delete_specific_watch(user_id: str, movie_id: str):
    """
    Remove a specific movie from a user's watch history.
    """
    if watch_collection is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    result = watch_collection.delete_one({"user_id": user_id, "movie_id": movie_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Watch record not found")
        
    return {"message": f"Successfully removed movie {movie_id} from user {user_id}'s history"}
