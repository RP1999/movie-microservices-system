from __future__ import annotations
from datetime import datetime, UTC
from pathlib import Path
from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.db.mongo import get_movies_collection
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate

ALLOWED_THUMBNAIL_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi"}

def _parse_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid movie ID format.")

def _escape_regex(value: str) -> str:
    return "".join(f"[{c}]" if c in r"[]\^$.|?*+(){}" else c for c in value)

def serialize_movie(doc: dict) -> MovieResponse:
    movie_id = str(doc["_id"])
    return MovieResponse(
        id=movie_id,
        title=doc["title"],
        category=doc["category"],
        thumbnail_url=_get_thumbnail_url(movie_id),
        video_url=_get_video_url(movie_id),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )

def _get_thumbnail_url(movie_id: str) -> str | None:
    files = list(settings.thumbnails_dir.glob(f"{movie_id}.*"))
    return f"/uploads/thumbnails/{files[0].name}" if files else None

def _get_video_url(movie_id: str) -> str | None:
    files = list(settings.videos_dir.glob(f"{movie_id}.*"))
    return f"/uploads/videos/{files[0].name}" if files else None

async def create_indexes() -> None:
    collection = await get_movies_collection()
    await collection.create_index("title")
    await collection.create_index("category")

async def list_movies(*, search: str | None = None, category: str | None = None, sort: str = "latest") -> list[MovieResponse]:
    collection = await get_movies_collection()
    filters = []
    if search:
        regex = {"$regex": _escape_regex(search), "$options": "i"}
        filters.append({"$or": [{"title": regex}, {"category": regex}]})
    if category:
        filters.append({"category": {"$regex": f"^{_escape_regex(category)}$", "$options": "i"}})
    query = {"$and": filters} if filters else {}
    sort_map = {"latest": [("created_at", -1)], "oldest": [("created_at", 1)], "title": [("title", 1)]}
    cursor = collection.find(query).sort(sort_map.get(sort, sort_map["latest"]))
    return [serialize_movie(doc) async for doc in cursor]

async def get_movie_by_id(movie_id: str) -> MovieResponse:
    collection = await get_movies_collection()
    doc = await collection.find_one({"_id": _parse_object_id(movie_id)})
    if not doc: raise HTTPException(status_code=404, detail="Movie not found.")
    return serialize_movie(doc)

async def create_movie(payload: MovieCreate, thumbnail: UploadFile | None = None, movie_file: UploadFile | None = None) -> MovieResponse:
    collection = await get_movies_collection()
    now = datetime.now(UTC)
    doc = {"title": payload.title, "category": payload.category, "created_at": now, "updated_at": now}
    result = await collection.insert_one(doc)
    movie_id = str(result.inserted_id)
    if thumbnail:
        ext = Path(thumbnail.filename).suffix
        (settings.thumbnails_dir / f"{movie_id}{ext}").write_bytes(await thumbnail.read())
    if movie_file:
        ext = Path(movie_file.filename).suffix
        (settings.videos_dir / f"{movie_id}{ext}").write_bytes(await movie_file.read())
    created = await collection.find_one({"_id": result.inserted_id})
    return serialize_movie(created)

async def update_movie(movie_id: str, payload: MovieUpdate, thumbnail: UploadFile | None = None, movie_file: UploadFile | None = None) -> MovieResponse:
    collection = await get_movies_collection()
    obj_id = _parse_object_id(movie_id)
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        updates["updated_at"] = datetime.now(UTC)
        await collection.update_one({"_id": obj_id}, {"$set": updates})
    if thumbnail:
        ext = Path(thumbnail.filename).suffix
        (settings.thumbnails_dir / f"{movie_id}{ext}").write_bytes(await thumbnail.read())
    if movie_file:
        ext = Path(movie_file.filename).suffix
        (settings.videos_dir / f"{movie_id}{ext}").write_bytes(await movie_file.read())
    updated = await collection.find_one({"_id": obj_id})
    return serialize_movie(updated)

async def delete_movie(movie_id: str) -> dict[str, str]:
    collection = await get_movies_collection()
    await collection.delete_one({"_id": _parse_object_id(movie_id)})
    return {"message": "Movie deleted successfully."}
