# user-service/main.py
from fastapi import FastAPI
from routes import router
from db import db
import uvicorn

app = FastAPI(
    title="User Service",
    version="1.0.0",
    description="User management service for movie streaming platform"
)

# Include routes
app.include_router(router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event"""
    if db is not None:
        print("✓ Application started - Connected to MongoDB")
    else:
        print("✗ Application started - MongoDB connection failed")

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "user-service",
        "port": 8001,
        "database": "mongodb"
    }

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "User Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "port": 8001
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
