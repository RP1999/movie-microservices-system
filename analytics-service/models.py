from pydantic import BaseModel
from typing import Optional

class MovieWatchData(BaseModel):
    movie_id: str
    title: str
    genre: str
    watch_count: int = 1
    total_watch_time_minutes: int

class UpdateMovieWatchData(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    watch_count: Optional[int] = None
    total_watch_time_minutes: Optional[int] = None
