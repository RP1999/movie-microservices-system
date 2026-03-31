from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.db.mongo import close_mongo_connection, connect_to_mongo, get_last_connection_error, ping_database
from app.routes.movies import router as movie_router
from app.services.movie_service import create_indexes

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await connect_to_mongo()
        await create_indexes()
    except Exception:
        pass
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Movie Service API",
    description="Movie catalog microservice for the Movie Streaming Platform assignment.",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(movie_router)
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")

@app.get("/", include_in_schema=False)
async def service_overview() -> dict[str, str]:
    return {"message": "Movie Service backend is running.", "docs": "/docs", "health": "/health", "api": "/api/movies"}

@app.get("/health", tags=["System"], summary="Health check")
async def health_check() -> dict[str, str | None]:
    db_ready = await ping_database()
    return {
        "status": "ok" if db_ready else "degraded",
        "service": settings.app_name,
        "port": str(settings.port),
        "database_status": "connected" if db_ready else "unavailable",
        "database_error": None if db_ready else get_last_connection_error(),
    }
