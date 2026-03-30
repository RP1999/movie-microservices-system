from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from bson import ObjectId
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.db.mongo import get_movies_collection
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate


ALLOWED_THUMBNAIL_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}


def serialize_movie(document: dict) -> MovieResponse:
    movie_id = str(document["_id"])
    created_at = document.get("created_at") or datetime.now(UTC)
    updated_at = document.get("updated_at") or created_at

    return MovieResponse(
        id=movie_id,
        title=document["title"],
        category=document["category"],
        thumbnail_url=_thumbnail_url(movie_id),
        video_url=_video_url(movie_id),
        created_at=created_at,
        updated_at=updated_at,
    )


def _escape_regex(value: str) -> str:
    return re.escape(value.strip())


def _parse_object_id(movie_id: str) -> ObjectId:
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid movie ID.")
    return ObjectId(movie_id)


def _thumbnail_files(movie_id: str) -> list[Path]:
    return sorted(settings.thumbnails_dir.glob(f"{movie_id}.*"))


def _thumbnail_url(movie_id: str) -> str | None:
    files = _thumbnail_files(movie_id)
    if not files:
        return None
    return f"/uploads/thumbnails/{files[0].name}"


def _video_files(movie_id: str) -> list[Path]:
    return sorted(settings.videos_dir.glob(f"{movie_id}.*"))


def _video_url(movie_id: str) -> str | None:
    files = _video_files(movie_id)
    if not files:
        return None
    return f"/uploads/videos/{files[0].name}"


def _delete_thumbnail_files(movie_id: str) -> None:
    for file_path in _thumbnail_files(movie_id):
        file_path.unlink(missing_ok=True)


def _delete_video_files(movie_id: str) -> None:
    for file_path in _video_files(movie_id):
        file_path.unlink(missing_ok=True)


async def _prepare_upload(
    upload: UploadFile | None,
    *,
    allowed_extensions: set[str],
    file_label: str,
) -> tuple[bytes, str] | None:
    if upload is None or not upload.filename:
        return None

    extension = Path(upload.filename).suffix.lower()
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{file_label} must use one of: {', '.join(sorted(allowed_extensions))}.",
        )

    content = await upload.read()
    await upload.close()

    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{file_label} is empty.")

    return content, extension


def _write_thumbnail(movie_id: str, prepared_thumbnail: tuple[bytes, str] | None) -> None:
    if prepared_thumbnail is None:
        return

    content, extension = prepared_thumbnail
    _delete_thumbnail_files(movie_id)
    target = settings.thumbnails_dir / f"{movie_id}{extension}"
    target.write_bytes(content)


def _write_video(movie_id: str, prepared_video: tuple[bytes, str] | None) -> None:
    if prepared_video is None:
        return

    content, extension = prepared_video
    _delete_video_files(movie_id)
    target = settings.videos_dir / f"{movie_id}{extension}"
    target.write_bytes(content)


async def _collection():
    try:
        return await get_movies_collection()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unavailable. Check the MongoDB Atlas connection. {exc}",
        ) from exc


async def create_indexes() -> None:
    collection = await _collection()
    await collection.create_index("title")
    await collection.create_index("category")
    await collection.create_index("created_at")


async def list_movies(
    *,
    search: str | None = None,
    category: str | None = None,
    sort: str = "latest",
) -> list[MovieResponse]:
    collection = await _collection()
    filters: list[dict] = []

    if search:
        regex = {"$regex": _escape_regex(search), "$options": "i"}
        filters.append({"$or": [{"title": regex}, {"category": regex}]})

    if category:
        filters.append({"category": {"$regex": f"^{_escape_regex(category)}$", "$options": "i"}})

    query = {"$and": filters} if filters else {}
    sort_map = {
        "latest": [("created_at", -1)],
        "oldest": [("created_at", 1)],
        "title": [("title", 1)],
        "category": [("category", 1), ("title", 1)],
    }
    ordering = sort_map.get(sort, sort_map["latest"])

    items: list[MovieResponse] = []
    cursor = collection.find(query).sort(ordering)
    async for document in cursor:
        items.append(serialize_movie(document))
    return items


async def get_movie_by_id(movie_id: str) -> MovieResponse:
    collection = await _collection()
    document = await collection.find_one({"_id": _parse_object_id(movie_id)})

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    return serialize_movie(document)


async def create_movie(
    payload: MovieCreate,
    thumbnail: UploadFile | None = None,
    movie_file: UploadFile | None = None,
) -> MovieResponse:
    collection = await _collection()
    prepared_thumbnail = await _prepare_upload(
        thumbnail,
        allowed_extensions=ALLOWED_THUMBNAIL_EXTENSIONS,
        file_label="Thumbnail",
    )
    prepared_video = await _prepare_upload(
        movie_file,
        allowed_extensions=ALLOWED_VIDEO_EXTENSIONS,
        file_label="Movie file",
    )
    now = datetime.now(UTC)
    document = {
        "title": payload.title,
        "category": payload.category,
        "created_at": now,
        "updated_at": now,
    }

    result = await collection.insert_one(document)
    movie_id = str(result.inserted_id)
    _write_thumbnail(movie_id, prepared_thumbnail)
    _write_video(movie_id, prepared_video)

    created = await collection.find_one({"_id": result.inserted_id})
    if created is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie creation failed.")
    return serialize_movie(created)


async def update_movie(
    movie_id: str,
    payload: MovieUpdate,
    thumbnail: UploadFile | None = None,
    movie_file: UploadFile | None = None,
) -> MovieResponse:
    collection = await _collection()
    updates = payload.model_dump(exclude_unset=True)
    prepared_thumbnail = await _prepare_upload(
        thumbnail,
        allowed_extensions=ALLOWED_THUMBNAIL_EXTENSIONS,
        file_label="Thumbnail",
    )
    prepared_video = await _prepare_upload(
        movie_file,
        allowed_extensions=ALLOWED_VIDEO_EXTENSIONS,
        file_label="Movie file",
    )

    if not updates and prepared_thumbnail is None and prepared_video is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update.")

    object_id = _parse_object_id(movie_id)
    if updates:
        updates["updated_at"] = datetime.now(UTC)
        result = await collection.update_one({"_id": object_id}, {"$set": updates})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")
    else:
        existing = await collection.find_one({"_id": object_id})
        if existing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    _write_thumbnail(movie_id, prepared_thumbnail)
    _write_video(movie_id, prepared_video)

    updated = await collection.find_one({"_id": object_id})
    if updated is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Movie update failed.")
    return serialize_movie(updated)


async def delete_movie(movie_id: str) -> dict[str, str]:
    collection = await _collection()
    result = await collection.delete_one({"_id": _parse_object_id(movie_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    _delete_thumbnail_files(movie_id)
    _delete_video_files(movie_id)
    return {"message": "Movie deleted successfully."}
