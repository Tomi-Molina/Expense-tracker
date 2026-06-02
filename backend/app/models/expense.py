from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ExpenseBase(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    date: datetime
    description: str = Field(min_length=1, max_length=500)

    @field_validator("category", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date: Optional[datetime] = None
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)

    @field_validator("category", "description")
    @classmethod
    def strip_text(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value


class ExpenseOut(ExpenseBase):
    id: str
    user_id: str