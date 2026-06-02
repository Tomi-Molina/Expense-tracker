from bson import ObjectId


class ExpenseRepository:
    def __init__(self, db):
        self.collection = db["expenses"]

    @staticmethod
    def serialize(doc: dict) -> dict:
        return {
            "id": str(doc["_id"]),
            "user_id": str(doc["user_id"]),
            "amount": doc["amount"],
            "category": doc["category"],
            "date": doc["date"],
            "description": doc["description"],
        }

    async def create(self, data: dict) -> dict:
        result = await self.collection.insert_one(data)
        doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.serialize(doc)

    async def list_by_user(self, user_id: str) -> list[dict]:
        cursor = self.collection.find({"user_id": ObjectId(user_id)}).sort("date", -1)
        return [self.serialize(doc) async for doc in cursor]

    async def get_by_id_and_user(self, expense_id: str, user_id: str) -> dict | None:
        if not ObjectId.is_valid(expense_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(expense_id), "user_id": ObjectId(user_id)})
        return self.serialize(doc) if doc else None

    async def update(self, expense_id: str, user_id: str, update_data: dict) -> dict | None:
        if not ObjectId.is_valid(expense_id):
            return None
        await self.collection.update_one(
            {"_id": ObjectId(expense_id), "user_id": ObjectId(user_id)},
            {"$set": update_data},
        )
        return await self.get_by_id_and_user(expense_id, user_id)

    async def delete(self, expense_id: str, user_id: str) -> bool:
        if not ObjectId.is_valid(expense_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(expense_id), "user_id": ObjectId(user_id)})
        return result.deleted_count == 1
