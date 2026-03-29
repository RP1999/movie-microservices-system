"""
Data models for Watchlist Service
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class WatchStatus(str, Enum):
    """Watch status options"""
    PLAN_TO_WATCH = "plan_to_watch"
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class AddToWatchlistRequest(BaseModel):
    """Request model for adding movie to watchlist"""
    user_id: int = Field(..., gt=0, description="User ID")
    movie_id: int = Field(..., gt=0, description="Movie ID")
    title: str = Field(..., min_length=1, max_length=200, description="Movie title")
    poster_url: Optional[str] = Field(None, description="Movie poster URL")
    year: Optional[int] = Field(None, ge=1900, le=2026, description="Release year")
    status: WatchStatus = Field(default=WatchStatus.PLAN_TO_WATCH, description="Watch status")
    notes: Optional[str] = Field(None, max_length=500, description="Personal notes")


class RemoveFromWatchlistRequest(BaseModel):
    """Request model for removing movie"""
    user_id: int = Field(..., gt=0)
    movie_id: int = Field(..., gt=0)


class MarkFavoriteRequest(BaseModel):
    """Request model for favorite marking"""
    user_id: int = Field(..., gt=0)
    movie_id: int = Field(..., gt=0)
    is_favorite: bool = Field(..., description="True to mark as favorite")


class UpdateStatusRequest(BaseModel):
    """Request model for status update"""
    user_id: int = Field(..., gt=0)
    movie_id: int = Field(..., gt=0)
    status: WatchStatus = Field(..., description="New watch status")
    notes: Optional[str] = Field(None, max_length=500)


class SortOption(str, Enum):
    """Sorting options"""
    DATE_ADDED_ASC = "date_added_asc"
    DATE_ADDED_DESC = "date_added_desc"
    TITLE_ASC = "title_asc"
    TITLE_DESC = "title_desc"
    STATUS = "status"
    FAVORITE_FIRST = "favorite_first"


class SortWatchlistRequest(BaseModel):
    """Request model for sorting"""
    user_id: int = Field(..., gt=0)
    sort_by: SortOption = Field(..., description="Sorting criteria")


class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool
    message: str
    data: Optional[dict] = None