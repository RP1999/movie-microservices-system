# user-service/db.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# MongoDB connection string
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.ncxtapi.mongodb.net/movie_system"

try:
    # Create MongoDB client
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    print("✓ Connected to MongoDB successfully")
except ConnectionFailure:
    print("✗ Failed to connect to MongoDB")
    client = None

# Get database
db = client['movie_system'] if client is not None else None

# Collections
if db is not None:
    users_collection = db['users']
    print("✓ Database and collection initialized")
else:
    users_collection = None
    print("✗ Database and collection not initialized")
