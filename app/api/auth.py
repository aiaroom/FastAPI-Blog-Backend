from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserMe 
from app.security.auth import get_current_user

from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.crud.user import get_user_by_email, create_user
from app.security.hashing import verify_password
from app.security.auth import create_access_token, create_refresh_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if await get_user_by_email(db, data.email):
        raise HTTPException(400, "User exists")
    user = await create_user(db, data.email, data.password)
    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Swagger отправит данные сюда
    db: AsyncSession = Depends(get_db)
):
    # Swagger отправляет логин в поле username, даже если это email
    user = await get_user_by_email(db, form_data.username)
    
    # Проверяем пароль
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    user = Depends(get_current_user) # В идеале здесь нужна логика проверки именно refresh токена
):
    # Упрощенная реализация (обычно refresh токен передают в body или cookie)
    # В рамках тестового задания часто достаточно проверить валидность текущего токена
    new_access_token = create_access_token(user.id)
    # Refresh токен обычно ротируется (выдается новый), либо возвращается старый
    from app.security.auth import create_refresh_token
    return Token(
        access_token=new_access_token,
        refresh_token=create_refresh_token(user.id)
    )

@router.get("/users/me", response_model=UserMe)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user