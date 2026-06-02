from bson import ObjectId


class UserRepository:
    def __init__(self, db):
        self.collection = db["users"]

    async def create(self, email: str, hashed_password: str) -> dict:
        result = await self.collection.insert_one({"email": email.lower(), "hashed_password": hashed_password})
        return await self.get_by_id(str(result.inserted_id))

    async def get_by_email(self, email: str) -> dict | None:
        return await self.collection.find_one({"email": email.lower()})

    async def get_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})
