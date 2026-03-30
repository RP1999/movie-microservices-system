from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.core.config import settings


client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None
last_connection_error: str | None = None


async def connect_to_mongo() -> None:
    global client, database, last_connection_error

    if not settings.mongodb_uri:
        raise RuntimeError("MONGODB_URI is not configured.")

    if client is not None and database is not None:
        return

    new_client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
    )

    try:
        await new_client.admin.command("ping")
    except Exception as exc:
        last_connection_error = str(exc)
        new_client.close()
        raise

    client = new_client
    database = client[settings.mongodb_db]
    last_connection_error = None


async def close_mongo_connection() -> None:
    global client, database, last_connection_error

    if client is not None:
        client.close()

    client = None
    database = None
    last_connection_error = None


async def ensure_connection() -> None:
    if database is None:
        await connect_to_mongo()


async def ping_database() -> bool:
    try:
        await ensure_connection()
        if client is None:
            return False
        await client.admin.command("ping")
        return True
    except Exception:
        return False


def get_last_connection_error() -> str | None:
    return last_connection_error


def get_database() -> AsyncIOMotorDatabase:
    if database is None:
        raise RuntimeError("Database connection has not been initialized.")
    return database


async def get_movies_collection() -> AsyncIOMotorCollection:
    await ensure_connection()
    return get_database()["movies"]
