from __future__ import annotations

from fastapi import APIRouter, File, Form, Query, UploadFile, status

from app.schemas.movie import DeleteResponse, MovieCreate, MovieResponse, MovieUpdate
from app.services.movie_service import (
    create_movie,
    delete_movie,
    get_movie_by_id,
    list_movies,
    update_movie,
)


router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.get("", response_model=list[MovieResponse], summary="Get all movies")
async def get_movies(
    search: str | None = Query(default=None, description="Search by title or category."),
    category: str | None = Query(default=None, description="Filter by category."),
    sort: str = Query(default="latest", description="Sort by latest, oldest, title, or category."),
) -> list[MovieResponse]:
    return await list_movies(search=search, category=category, sort=sort)


@router.get("/{movie_id}", response_model=MovieResponse, summary="Get movie by ID")
async def get_movie(movie_id: str) -> MovieResponse:
    return await get_movie_by_id(movie_id)


@router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED, summary="Add a new movie")
async def add_movie(
    title: str = Form(...),
    category: str = Form(...),
    thumbnail: UploadFile | None = File(default=None),
    movie_file: UploadFile | None = File(default=None),
) -> MovieResponse:
    return await create_movie(MovieCreate(title=title, category=category), thumbnail, movie_file)


@router.put("/{movie_id}", response_model=MovieResponse, summary="Update movie details")
async def edit_movie(
    movie_id: str,
    title: str | None = Form(default=None),
    category: str | None = Form(default=None),
    thumbnail: UploadFile | None = File(default=None),
    movie_file: UploadFile | None = File(default=None),
) -> MovieResponse:
    return await update_movie(movie_id, MovieUpdate(title=title, category=category), thumbnail, movie_file)


@router.delete("/{movie_id}", response_model=DeleteResponse, summary="Delete movie")
async def remove_movie(movie_id: str) -> DeleteResponse:
    return DeleteResponse(**(await delete_movie(movie_id)))
