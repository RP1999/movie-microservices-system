# Movie Service

Movie Service for the Movie Streaming Platform assignment.

Tech stack:
- FastAPI backend
- MongoDB Atlas

Service details:
- Direct service port: `8002`
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`
- Health check: `http://localhost:8002/health`
- Movie API base: `http://localhost:8002/api/movies`

Implemented features:
- Add new movie
- Update movie details
- Delete movie
- Get all movies
- Get movie by ID
- Search movies by title or category
- Filter movies by category
- Upload thumbnail locally
- Upload movie file locally

## Setup

1. Install backend dependencies:

```bash
pip install -r requirements.txt
```

2. Run the FastAPI service:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

## Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

## Environment

Copy `.env.example` to `.env` if needed. The local `.env` is ignored by git.

Required variables:
- `PORT=8002`
- `MONGODB_URI=...`
- `MONGODB_DB=movie_system`
- `GATEWAY_BASE_URL=http://localhost:8000/movies`

Storage design:
- MongoDB stores only `title` and `category`
- Thumbnails are stored locally in `app/uploads/thumbnails`
- Movie/video files are stored locally in `app/uploads/videos`

## Suggested API Gateway Route

The API gateway can proxy:

- `/movies/*` -> `http://localhost:8002/*`

That gives you:
- Direct Swagger: `http://localhost:8002/docs`
- Gateway Swagger: `http://localhost:8000/movies/docs`
