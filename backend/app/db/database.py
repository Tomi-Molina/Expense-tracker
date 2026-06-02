from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


async def connect_to_mongo() -> None:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)


async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_database():
    if _client is None:
        raise RuntimeError("MongoDB client is not initialized")
    return _client[settings.mongodb_db]
