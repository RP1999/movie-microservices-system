from fastapi import FastAPI
from app.routes.review_routes import router as review_router

app = FastAPI(title="Review & Rating Service")

# Root route for testing
@app.get("/")
def root():
    return {"message": "Review & Rating Service is running!"}

# Include your review router
app.include_router(review_router, prefix="/reviews", tags=["Reviews"])