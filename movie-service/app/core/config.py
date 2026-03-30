from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    app_name = "Movie Service"
    app_version = "1.0.0"
    port = int(os.getenv("PORT", "8002"))
    mongodb_uri = os.getenv("MONGODB_URI", "")
    mongodb_db = os.getenv("MONGODB_DB", "movie_system")
    gateway_base_url = os.getenv("GATEWAY_BASE_URL", "http://localhost:8000/movies")
    uploads_dir = BASE_DIR / "app" / "uploads"
    thumbnails_dir = uploads_dir / "thumbnails"
    videos_dir = uploads_dir / "videos"


settings = Settings()
settings.thumbnails_dir.mkdir(parents=True, exist_ok=True)
settings.videos_dir.mkdir(parents=True, exist_ok=True)
