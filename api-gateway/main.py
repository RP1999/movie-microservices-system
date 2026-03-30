from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import StreamingResponse
from typing import Any
import httpx

app = FastAPI(
    title="Movie Streaming API Gateway",
    description="""
API Gateway for the Movie Streaming & Recommendation Microservice System.

This gateway provides a single entry point to access all microservices.
All requests go through this gateway and are routed to the appropriate microservice.
    """,
    version="1.0.0"
)

# Configuration for underlying services
SERVICES = {
    "streaming": "http://localhost:8003",   # Ranidu's part
    "watchlist": "http://localhost:8004",   # Siluni's part
    "review":    "http://localhost:8005",   # Piyumi's part
    "user":      "http://localhost:8001",   # Lashan's part
    # "movie":   "http://localhost:8002",   # Shevin's part
    # "analytics":"http://localhost:8006",  # Dilina's part
}

# ─────────────────────────────────────────────
# Helper: Forward any request to a microservice
# ─────────────────────────────────────────────
async def forward(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
    target_url = f"{SERVICES[service]}/{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    async with httpx.AsyncClient() as client:
        try:
            req = client.build_request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
                params=request.query_params,
            )
            resp = await client.send(req, stream=True)
            return StreamingResponse(
                resp.aiter_raw(),
                status_code=resp.status_code,
                headers=dict(resp.headers),
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Cannot reach {service} service: {e}")


# ══════════════════════════════════════════════════════════
# GATEWAY INFO
# ══════════════════════════════════════════════════════════

@app.get("/", tags=["Gateway Info"])
async def gateway_home():
    """Health check for the API Gateway — confirms the gateway is live."""
    return {
        "message": "Movie Streaming API Gateway is running",
        "version": "1.0.0",
        "services": list(SERVICES.keys()),
    }


# ══════════════════════════════════════════════════════════
# STREAMING SERVICE  (Ranidu — Port 8003)
# ══════════════════════════════════════════════════════════

@app.get("/streaming/stream/{movie_id}", tags=["Streaming Service"])
async def get_stream(movie_id: str, request: Request):
    """Get the streaming URL for a specific movie."""
    return await forward("streaming", f"stream/{movie_id}", request)

@app.post("/streaming/watch", tags=["Streaming Service"])
async def save_watch(request: Request, payload: Any = Body(default=None)):
    """Record that a user started watching a movie. Body: {user_id, movie_id}"""
    return await forward("streaming", "watch", request)

@app.get("/streaming/watch/{user_id}", tags=["Streaming Service"])
async def get_watch_history(user_id: str, request: Request):
    """Get the full watch history for a specific user."""
    return await forward("streaming", f"watch/{user_id}", request)

@app.put("/streaming/watch/progress", tags=["Streaming Service"])
async def update_watch_progress(request: Request, payload: Any = Body(default=None)):
    """Save the user's current progress (pause point) for a movie. Body: {user_id, movie_id, progress_minutes}"""
    return await forward("streaming", "watch/progress", request)

@app.delete("/streaming/watch/{user_id}", tags=["Streaming Service"])
async def clear_watch_history(user_id: str, request: Request):
    """Delete all watch history for a specific user."""
    return await forward("streaming", f"watch/{user_id}", request)


# ══════════════════════════════════════════════════════════
# WATCHLIST SERVICE  (Siluni — Port 8004)
# ══════════════════════════════════════════════════════════

@app.post("/watchlist/add", tags=["Watchlist Service"])
async def add_to_watchlist(request: Request, payload: Any = Body(default=None)):
    """Add a movie to a user's watchlist. Body: {user_id, movie_id}"""
    return await forward("watchlist", "api/watchlist/add", request)

@app.delete("/watchlist/remove", tags=["Watchlist Service"])
async def remove_from_watchlist(request: Request, payload: Any = Body(default=None)):
    """Remove a specific movie from a user's watchlist. Body: {user_id, movie_id}"""
    return await forward("watchlist", "api/watchlist/remove", request)

@app.get("/watchlist/{user_id}", tags=["Watchlist Service"])
async def get_watchlist(user_id: int, request: Request):
    """Get the full watchlist for a specific user."""
    return await forward("watchlist", f"api/watchlist/{user_id}", request)

@app.patch("/watchlist/favorite", tags=["Watchlist Service"])
async def mark_favorite(request: Request, payload: Any = Body(default=None)):
    """Mark or unmark a movie as a favourite. Body: {user_id, movie_id, is_favorite}"""
    return await forward("watchlist", "api/watchlist/favorite", request)

@app.delete("/watchlist/clear/{user_id}", tags=["Watchlist Service"])
async def clear_watchlist(user_id: int, request: Request):
    """Clear the entire watchlist for a specific user."""
    return await forward("watchlist", f"api/watchlist/clear/{user_id}", request)

@app.post("/watchlist/sort", tags=["Watchlist Service"])
async def sort_watchlist(request: Request, payload: Any = Body(default=None)):
    """Sort a user's watchlist by a given criteria. Body: {user_id, sort_by}"""
    return await forward("watchlist", "api/watchlist/sort", request)

@app.patch("/watchlist/status", tags=["Watchlist Service"])
async def update_watchlist_status(request: Request, payload: Any = Body(default=None)):
    """Update the watch-status of a movie on the watchlist. Body: {user_id, movie_id, status}"""
    return await forward("watchlist", "api/watchlist/status", request)

@app.get("/watchlist/stats/{user_id}", tags=["Watchlist Service"])
async def get_watchlist_stats(user_id: int, request: Request):
    """Get watchlist statistics for a specific user."""
    return await forward("watchlist", f"api/watchlist/stats/{user_id}", request)

@app.get("/watchlist/check/{user_id}/{movie_id}", tags=["Watchlist Service"])
async def check_in_watchlist(user_id: int, movie_id: int, request: Request):
    """Check whether a specific movie is in a user's watchlist."""
    return await forward("watchlist", f"api/watchlist/check/{user_id}/{movie_id}", request)


# ══════════════════════════════════════════════════════════
# REVIEW SERVICE  (Piyumi — Port 8005)
# ══════════════════════════════════════════════════════════

@app.post("/reviews", tags=["Review Service"])
async def create_review(request: Request, payload: Any = Body(default=None)):
    """Create a new movie review. Body: {movie_id, user_id, rating, comment}"""
    return await forward("review", "reviews/", request)

@app.put("/reviews/{review_id}", tags=["Review Service"])
async def update_review(review_id: str, request: Request, payload: Any = Body(default=None)):
    """Update an existing review by its ID."""
    return await forward("review", f"reviews/{review_id}", request)

@app.delete("/reviews/{review_id}", tags=["Review Service"])
async def delete_review(review_id: str, request: Request):
    """Delete a review by its ID."""
    return await forward("review", f"reviews/{review_id}", request)

@app.get("/reviews/movie/{movie_id}", tags=["Review Service"])
async def get_reviews_by_movie(movie_id: str, request: Request):
    """Get all reviews for a specific movie."""
    return await forward("review", f"reviews/movie/{movie_id}", request)

@app.get("/reviews/movie/{movie_id}/average-rating", tags=["Review Service"])
async def get_average_rating(movie_id: str, request: Request):
    """Get the average rating for a specific movie."""
    return await forward("review", f"reviews/movie/{movie_id}/average-rating", request)

@app.post("/reviews/{review_id}/like", tags=["Review Service"])
async def like_review(review_id: str, request: Request):
    """Like a specific review."""
    return await forward("review", f"reviews/{review_id}/like", request)

@app.post("/reviews/{review_id}/dislike", tags=["Review Service"])
async def dislike_review(review_id: str, request: Request):
    """Dislike a specific review."""
    return await forward("review", f"reviews/{review_id}/dislike", request)


# ══════════════════════════════════════════════════════════
# USER SERVICE  (Lashan — Port 8001)
# ══════════════════════════════════════════════════════════

@app.post("/users/auth/register", tags=["User Service"])
async def register_user(request: Request, payload: Any = Body(default=None)):
    """Register a new user. Body: {name, email, password, age}"""
    return await forward("user", "api/auth/register", request)

@app.post("/users/auth/login", tags=["User Service"])
async def login_user(request: Request, payload: Any = Body(default=None)):
    """Login with email and password. Body: {email, password}"""
    return await forward("user", "api/auth/login", request)

@app.post("/users/auth/reset-password", tags=["User Service"])
async def reset_password(request: Request, payload: Any = Body(default=None)):
    """Reset user password using a reset token. Body: {reset_token, new_password, confirm_password}"""
    return await forward("user", "api/auth/reset-password", request)

@app.post("/users/auth/verify-email", tags=["User Service"])
async def verify_email(request: Request, payload: Any = Body(default=None)):
    """Verify user email with a token. Body: {email, verification_token}"""
    return await forward("user", "api/auth/email-verification/verify", request)

@app.get("/users/{user_id}", tags=["User Service"])
async def get_user(user_id: int, request: Request):
    """Get user profile by user ID."""
    return await forward("user", f"api/users/{user_id}", request)

@app.put("/users/{user_id}", tags=["User Service"])
async def update_user(user_id: int, request: Request, payload: Any = Body(default=None)):
    """Update user profile (name, age, preferences). Body: {name, age, preferences}"""
    return await forward("user", f"api/users/{user_id}", request)

@app.delete("/users/{user_id}", tags=["User Service"])
async def delete_user(user_id: int, request: Request):
    """Deactivate a user account."""
    return await forward("user", f"api/users/{user_id}", request)

@app.get("/users/admin/all-admins", tags=["User Service"])
async def get_admins(request: Request):
    """Get all users with the admin role."""
    return await forward("user", "api/admin/users/role/admin", request)

@app.post("/users/admin/{user_id}/assign-role", tags=["User Service"])
async def assign_role_to_user(user_id: int, request: Request, payload: Any = Body(default=None)):
    """Assign an admin or user role to a specific user. Body: {role}"""
    return await forward("user", f"api/admin/users/{user_id}/role", request)
