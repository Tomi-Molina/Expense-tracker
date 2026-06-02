from fastapi import HTTPException, status
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, password: str) -> dict:
        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user = await self.user_repository.create(email=email, hashed_password=hash_password(password))
        return {"user": {"id": str(user["_id"]), "email": user["email"]}, "access_token": create_access_token(str(user["_id"]))}

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return {"user": {"id": str(user["_id"]), "email": user["email"]}, "access_token": create_access_token(str(user["_id"]))}
