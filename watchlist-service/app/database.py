"""
Database connection module with MongoDB
No fallback - will fail if MongoDB not connected
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

# Get MongoDB connection URL from environment
MONGODB_URL = os.getenv("MONGODB_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "watchlists")

# Global variables
client = None
database = None
watchlist_collection = None
is_connected = False


async def connect_to_mongo():
    """Establish connection to MongoDB"""
    global client, database, watchlist_collection, is_connected
    
    if not MONGODB_URL:
        print("ERROR: MONGODB_URL not set in environment variables!")
        is_connected = False
        return False
    
    try:
        print(f"Attempting to connect to MongoDB...")
        print(f"Using URL: {MONGODB_URL[:50]}...")  # Print first 50 chars for debugging
        
        # Create MongoDB client with proper options
        client = AsyncIOMotorClient(
            MONGODB_URL,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            maxPoolSize=10
        )
        
        # Test connection by pinging
        await client.admin.command('ping')
        print("SUCCESS: MongoDB ping successful!")
        
        # Get database - extract database name from URL
        # URL format: mongodb+srv://admin:admin123@cluster0.ncxtapi.mongodb.net/movie_system
        database_name = os.getenv("DATABASE_NAME")
        if not database_name:
            # Extract database name from URL if not in env
            if MONGODB_URL and "/" in MONGODB_URL:
                database_name = MONGODB_URL.split("/")[-1].split("?")[0]
            else:
                database_name = "movie_system"
        
        database = client[database_name]
        watchlist_collection = database[COLLECTION_NAME]
        
        # Create indexes for better performance
        await watchlist_collection.create_index("user_id")
        await watchlist_collection.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        
        is_connected = True
        print(f"SUCCESS: Connected to MongoDB Atlas: {database_name}")
        print(f"SUCCESS: Collection: {COLLECTION_NAME}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to MongoDB: {str(e)}")
        print(f"ERROR: Please check:")
        print(f"   - MongoDB URL is correct: {MONGODB_URL}")
        print(f"   - Network connection")
        print(f"   - Username/password")
        print(f"   - IP whitelist in MongoDB Atlas")
        is_connected = False
        return False


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client, is_connected
    if client:
        client.close()
        is_connected = False
        print("SUCCESS: MongoDB connection closed")


def get_collection():
    """Get watchlist collection - raises error if not connected"""
    if not is_connected or watchlist_collection is None:
        raise Exception("MongoDB not connected. Please check your connection.")
    return watchlist_collection


def is_database_connected():
    """Check if database is connected"""
    return is_connected