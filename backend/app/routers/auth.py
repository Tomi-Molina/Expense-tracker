from fastapi import APIRouter

from app.db.database import get_database
from app.models.token import Token
from app.models.user import UserCreate, UserLogin, UserOut
from app.repositories.users import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register")
async def register(payload: UserCreate) -> dict:
    db = get_database()
    result = await AuthService(UserRepository(db)).register(payload.email, payload.password)
    return {"access_token": result["access_token"], "token_type": "bearer", "user": result["user"]}


@router.post("/login")
async def login(payload: UserLogin) -> dict:
    db = get_database()
    result = await AuthService(UserRepository(db)).login(payload.email, payload.password)
    return {"access_token": result["access_token"], "token_type": "bearer", "user": result["user"]}
