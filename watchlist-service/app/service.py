"""
Business logic layer with MongoDB
"""

from datetime import datetime
from typing import Dict, Any
from app.database import get_collection, is_database_connected
from app.models import AddToWatchlistRequest, WatchStatus, SortOption


class WatchlistService:
    """Service class for watchlist operations with MongoDB"""
    
    def __init__(self):
        """Initialize service - will use MongoDB"""
        self.collection = None
    
    async def _get_collection(self):
        """Get collection, ensure it's available"""
        if not is_database_connected():
            raise Exception("MongoDB not connected. Service unavailable.")
        if self.collection is None:
            self.collection = get_collection()
        return self.collection
    
    async def add_to_watchlist(self, request: AddToWatchlistRequest) -> Dict[str, Any]:
        """Add movie to watchlist"""
        try:
            collection = await self._get_collection()
            
            # Check if movie already exists
            existing = await collection.find_one({
                "user_id": request.user_id,
                "movie_id": request.movie_id
            })
            
            if existing:
                return {
                    "success": False,
                    "message": "Movie already in watchlist",
                    "data": None
                }
            
            # Create new watchlist item
            watchlist_item = {
                "user_id": request.user_id,
                "movie_id": request.movie_id,
                "title": request.title,
                "poster_url": request.poster_url,
                "year": request.year,
                "added_at": datetime.now(),
                "is_favorite": False,
                "status": request.status.value,
                "notes": request.notes
            }
            
            # Insert into database
            result = await collection.insert_one(watchlist_item)
            
            return {
                "success": True,
                "message": "Movie added to watchlist",
                "data": {
                    "id": str(result.inserted_id),
                    "movie_id": request.movie_id,
                    "title": request.title
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def remove_from_watchlist(self, user_id: int, movie_id: int) -> Dict[str, Any]:
        """Remove movie from watchlist"""
        try:
            collection = await self._get_collection()
            
            result = await collection.delete_one({
                "user_id": user_id,
                "movie_id": movie_id
            })
            
            if result.deleted_count == 0:
                return {
                    "success": False,
                    "message": "Movie not found in watchlist",
                    "data": None
                }
            
            return {
                "success": True,
                "message": "Movie removed from watchlist",
                "data": {"user_id": user_id, "movie_id": movie_id}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def get_watchlist(self, user_id: int) -> Dict[str, Any]:
        """Get all watchlist items for user"""
        try:
            collection = await self._get_collection()
            
            cursor = collection.find({"user_id": user_id})
            items = await cursor.to_list(length=100)
            
            formatted_items = []
            for item in items:
                formatted_items.append({
                    "id": str(item["_id"]),
                    "movie_id": item["movie_id"],
                    "title": item["title"],
                    "poster_url": item.get("poster_url"),
                    "year": item.get("year"),
                    "added_at": item["added_at"].isoformat() if item["added_at"] else None,
                    "is_favorite": item["is_favorite"],
                    "status": item["status"],
                    "notes": item.get("notes")
                })
            
            return {
                "success": True,
                "message": f"Found {len(formatted_items)} items",
                "data": {
                    "user_id": user_id,
                    "total_items": len(formatted_items),
                    "items": formatted_items
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def mark_favorite(self, user_id: int, movie_id: int, is_favorite: bool) -> Dict[str, Any]:
        """Mark/unmark movie as favorite"""
        try:
            collection = await self._get_collection()
            
            result = await collection.update_one(
                {"user_id": user_id, "movie_id": movie_id},
                {"$set": {"is_favorite": is_favorite}}
            )
            
            if result.matched_count == 0:
                return {
                    "success": False,
                    "message": "Movie not found in watchlist",
                    "data": None
                }
            
            action = "marked as favorite" if is_favorite else "unmarked as favorite"
            return {
                "success": True,
                "message": f"Movie {action}",
                "data": {"user_id": user_id, "movie_id": movie_id, "is_favorite": is_favorite}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def clear_watchlist(self, user_id: int) -> Dict[str, Any]:
        """Clear entire watchlist"""
        try:
            collection = await self._get_collection()
            
            result = await collection.delete_many({"user_id": user_id})
            
            return {
                "success": True,
                "message": f"Cleared {result.deleted_count} items",
                "data": {"user_id": user_id, "items_cleared": result.deleted_count}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def sort_watchlist(self, user_id: int, sort_by: SortOption) -> Dict[str, Any]:
        """Sort watchlist items"""
        try:
            collection = await self._get_collection()
            
            cursor = collection.find({"user_id": user_id})
            items = await cursor.to_list(length=100)
            
            # Convert to list for sorting
            sortable_items = []
            for item in items:
                sortable_items.append({
                    "id": str(item["_id"]),
                    "movie_id": item["movie_id"],
                    "title": item["title"],
                    "poster_url": item.get("poster_url"),
                    "year": item.get("year"),
                    "added_at": item["added_at"],
                    "is_favorite": item["is_favorite"],
                    "status": item["status"],
                    "notes": item.get("notes")
                })
            
            # Apply sorting
            if sort_by == SortOption.DATE_ADDED_ASC:
                sortable_items.sort(key=lambda x: x["added_at"])
            elif sort_by == SortOption.DATE_ADDED_DESC:
                sortable_items.sort(key=lambda x: x["added_at"], reverse=True)
            elif sort_by == SortOption.TITLE_ASC:
                sortable_items.sort(key=lambda x: x["title"].lower())
            elif sort_by == SortOption.TITLE_DESC:
                sortable_items.sort(key=lambda x: x["title"].lower(), reverse=True)
            elif sort_by == SortOption.STATUS:
                sortable_items.sort(key=lambda x: x["status"])
            elif sort_by == SortOption.FAVORITE_FIRST:
                sortable_items.sort(key=lambda x: (not x["is_favorite"], x["title"].lower()))
            
            # Format dates
            for item in sortable_items:
                if item["added_at"]:
                    item["added_at"] = item["added_at"].isoformat()
            
            return {
                "success": True,
                "message": f"Sorted by {sort_by.value}",
                "data": {
                    "user_id": user_id,
                    "sort_by": sort_by.value,
                    "total_items": len(sortable_items),
                    "items": sortable_items
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def update_status(self, user_id: int, movie_id: int, status: WatchStatus, notes: str = None) -> Dict[str, Any]:
        """Update watch status and notes"""
        try:
            collection = await self._get_collection()
            
            update_data = {"status": status.value}
            if notes is not None:
                update_data["notes"] = notes
            
            result = await collection.update_one(
                {"user_id": user_id, "movie_id": movie_id},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return {
                    "success": False,
                    "message": "Movie not found in watchlist",
                    "data": None
                }
            
            return {
                "success": True,
                "message": f"Status updated to {status.value}",
                "data": {"user_id": user_id, "movie_id": movie_id, "status": status.value}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }
    
    async def get_stats(self, user_id: int) -> Dict[str, Any]:
        """Get watchlist statistics"""
        try:
            collection = await self._get_collection()
            
            cursor = collection.find({"user_id": user_id})
            items = await cursor.to_list(length=100)
            
            total = len(items)
            favorites = sum(1 for item in items if item["is_favorite"])
            
            status_counts = {}
            for item in items:
                status = item["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "success": True,
                "message": "Statistics retrieved",
                "data": {
                    "user_id": user_id,
                    "total_items": total,
                    "favorites_count": favorites,
                    "by_status": status_counts
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "data": None
            }