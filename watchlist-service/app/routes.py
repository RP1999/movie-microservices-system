"""
API Routes with proper error handling
"""

from fastapi import APIRouter, HTTPException, Path, Depends
from app.models import (
    AddToWatchlistRequest, RemoveFromWatchlistRequest,
    MarkFavoriteRequest, UpdateStatusRequest, SortWatchlistRequest,
    APIResponse
)
from app.service import WatchlistService
from app.database import is_database_connected

# Create router
router = APIRouter(prefix="/api/watchlist", tags=["Watchlist"])

# Initialize service
service = WatchlistService()


async def check_db_connection():
    """Dependency to check database connection"""
    if not is_database_connected():
        raise HTTPException(
            status_code=503,
            detail="Database connection not available. Please check MongoDB connection."
        )
    return True


@router.post("/add", response_model=APIResponse)
async def add_to_watchlist(request: AddToWatchlistRequest, db_ok: bool = Depends(check_db_connection)):
    """Add movie to watchlist"""
    result = await service.add_to_watchlist(request)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.delete("/remove", response_model=APIResponse)
async def remove_from_watchlist(request: RemoveFromWatchlistRequest, db_ok: bool = Depends(check_db_connection)):
    """Remove movie from watchlist"""
    result = await service.remove_from_watchlist(request.user_id, request.movie_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.get("/{user_id}", response_model=APIResponse)
async def get_watchlist(user_id: int = Path(..., gt=0), db_ok: bool = Depends(check_db_connection)):
    """Get user's watchlist"""
    result = await service.get_watchlist(user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.patch("/favorite", response_model=APIResponse)
async def mark_favorite(request: MarkFavoriteRequest, db_ok: bool = Depends(check_db_connection)):
    """Mark/unmark movie as favorite"""
    result = await service.mark_favorite(request.user_id, request.movie_id, request.is_favorite)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.delete("/clear/{user_id}", response_model=APIResponse)
async def clear_watchlist(user_id: int = Path(..., gt=0), db_ok: bool = Depends(check_db_connection)):
    """Clear entire watchlist"""
    result = await service.clear_watchlist(user_id)
    return result


@router.post("/sort", response_model=APIResponse)
async def sort_watchlist(request: SortWatchlistRequest, db_ok: bool = Depends(check_db_connection)):
    """Sort watchlist by criteria"""
    result = await service.sort_watchlist(request.user_id, request.sort_by)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.patch("/status", response_model=APIResponse)
async def update_status(request: UpdateStatusRequest, db_ok: bool = Depends(check_db_connection)):
    """Update watch status"""
    result = await service.update_status(
        request.user_id, request.movie_id, request.status, request.notes
    )
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@router.get("/stats/{user_id}", response_model=APIResponse)
async def get_stats(user_id: int = Path(..., gt=0), db_ok: bool = Depends(check_db_connection)):
    """Get watchlist statistics"""
    result = await service.get_stats(user_id)
    return result


@router.get("/check/{user_id}/{movie_id}", response_model=APIResponse)
async def check_in_watchlist(
    user_id: int = Path(..., gt=0),
    movie_id: int = Path(..., gt=0),
    db_ok: bool = Depends(check_db_connection)
):
    """Check if movie exists in watchlist"""
    watchlist = await service.get_watchlist(user_id)
    if watchlist["success"]:
        items = watchlist["data"]["items"]
        exists = any(item["movie_id"] == movie_id for item in items)
        return {
            "success": True,
            "message": "Check completed",
            "data": {"user_id": user_id, "movie_id": movie_id, "exists": exists}
        }
    return {
        "success": True,
        "message": "Check completed",
        "data": {"user_id": user_id, "movie_id": movie_id, "exists": False}
    }