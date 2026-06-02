from fastapi import APIRouter, Depends

from app.core.deps import get_current_user_id
from app.db.database import get_database
from app.models.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate
from app.repositories.expenses import ExpenseRepository
from app.services.expense_service import ExpenseService

router = APIRouter()


@router.get("", response_model=list[ExpenseOut])
async def list_expenses(user_id: str = Depends(get_current_user_id)):
    db = get_database()
    return await ExpenseService(ExpenseRepository(db)).list(user_id)


@router.post("", response_model=ExpenseOut)
async def create_expense(payload: ExpenseCreate, user_id: str = Depends(get_current_user_id)):
    db = get_database()
    return await ExpenseService(ExpenseRepository(db)).create(user_id, payload.model_dump())


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense(expense_id: str, user_id: str = Depends(get_current_user_id)):
    db = get_database()
    return await ExpenseService(ExpenseRepository(db)).get(user_id, expense_id)


@router.put("/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: str, payload: ExpenseUpdate, user_id: str = Depends(get_current_user_id)):
    db = get_database()
    return await ExpenseService(ExpenseRepository(db)).update(user_id, expense_id, payload.model_dump())


@router.delete("/{expense_id}")
async def delete_expense(expense_id: str, user_id: str = Depends(get_current_user_id)):
    db = get_database()
    await ExpenseService(ExpenseRepository(db)).delete(user_id, expense_id)
    return {"message": "Expense deleted successfully"}
