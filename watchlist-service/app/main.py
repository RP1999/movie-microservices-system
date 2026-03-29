"""
Main FastAPI application with MongoDB
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from app.routes import router
from app.database import connect_to_mongo, close_mongo_connection, is_database_connected

# Load environment variables
load_dotenv()

# Get port from environment or use 8004
PORT = int(os.getenv("PORT", 8004))

# Create FastAPI app
app = FastAPI(
    title="Watchlist Service API",
    description="Microservice for managing user watchlists with MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    print("\n" + "="*50)
    print("STARTING WATCHLIST SERVICE")
    print("="*50)
    print(f"Port: {PORT}")
    print(f"MongoDB URL from env: {os.getenv('MONGODB_URL', 'NOT SET!')}")
    print(f"Database Name from env: {os.getenv('DATABASE_NAME', 'NOT SET!')}")
    print(f"Collection Name: {os.getenv('COLLECTION_NAME', 'watchlists')}")
    print("-"*50)
    
    # Connect to MongoDB
    connected = await connect_to_mongo()
    
    if connected:
        print("SUCCESS: SERVICE READY - Connected to MongoDB Atlas")
    else:
        print("ERROR: SERVICE STARTED BUT MONGODB NOT CONNECTED")
        print("WARNING: API will return 503 errors until MongoDB connects")
        print("Please check:")
        print("1. MongoDB Atlas cluster is running")
        print("2. Network access (IP whitelist)")
        print("3. Username/password are correct")
        print("4. Connection string is correct")
    
    print("="*50 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()
    print("Service shutdown complete")


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "message": "Watchlist Service is running",
        "data": {
            "service": "watchlist-service",
            "version": "1.0.0",
            "port": PORT,
            "mongodb_connected": is_database_connected()
        }
    }


@app.get("/db-status", tags=["Health"])
async def db_status():
    """Check database connection status"""
    if is_database_connected():
        return {
            "success": True,
            "message": "MongoDB is connected",
            "data": {
                "status": "connected"
            }
        }
    else:
        raise HTTPException(
            status_code=503,
            detail="MongoDB not connected. Please check your connection settings."
        )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )