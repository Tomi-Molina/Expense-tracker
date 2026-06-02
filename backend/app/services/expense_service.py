from fastapi import HTTPException, status
from bson import ObjectId
from app.repositories.expenses import ExpenseRepository


class ExpenseService:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    async def create(self, user_id: str, data: dict) -> dict:
        payload = {
            "user_id": ObjectId(user_id),
            "amount": data["amount"],
            "category": data["category"],
            "date": data["date"],
            "description": data["description"],
        }
        return await self.expense_repository.create(payload)

    async def list(self, user_id: str) -> list[dict]:
        return await self.expense_repository.list_by_user(user_id)

    async def get(self, user_id: str, expense_id: str) -> dict:
        expense = await self.expense_repository.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        return expense

    async def update(self, user_id: str, expense_id: str, data: dict) -> dict:
        payload = {key: value for key, value in data.items() if value is not None}
        expense = await self.expense_repository.update(expense_id, user_id, payload)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        return expense

    async def delete(self, user_id: str, expense_id: str) -> None:
        deleted = await self.expense_repository.delete(expense_id, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
