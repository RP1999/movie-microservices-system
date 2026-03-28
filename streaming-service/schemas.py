from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import List, Optional

class StreamResponse(BaseModel):
    movie_id: str = Field(..., description="The unique identifier for the movie")
    stream_url: HttpUrl = Field(..., description="The URL to start streaming the movie")
    quality: str = Field(..., description="The quality of the video stream (e.g., 1080p)")
    status: str = Field(..., description="The status of the stream (e.g., ready)")

class WatchRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user watching the movie")
    movie_id: str = Field(..., description="The ID of the movie being watched")

class WatchRecord(BaseModel):
    user_id: str
    movie_id: str
    time: datetime
    progress_minutes: Optional[int] = None
    status: Optional[str] = None

class WatchProgressRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user watching the movie")
    movie_id: str = Field(..., description="The ID of the movie being watched")
    progress_minutes: int = Field(..., description="The minute mark the user paused the movie at")
