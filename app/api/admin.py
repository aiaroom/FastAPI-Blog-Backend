from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryOut
from app.schemas.post import PostCreate, PostOut
from app.crud.category import create_category
from app.crud.post import create_post
from app.security.auth import require_admin, get_current_user
from app.utils.sanitization import sanitize_html

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.post("/categories", response_model=CategoryOut)
async def create_cat(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    return await create_category(db, data.name, data.slug)


@router.post("/posts", response_model=PostOut)
async def create_new_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_admin),
):
    clean_html = sanitize_html(data.content_html)

    return await create_post(
        db,
        title=data.title,
        slug=data.slug,
        content_html=clean_html,
        category_id=data.category_id,
        author_id=user.id,
    )

from app.schemas.user import UserUpdate, User as UserSchema
from app.models.user import User
from sqlalchemy import select

@router.patch("/users/{user_id}/role", response_model=UserSchema)
async def change_user_role(
    user_id: int,
    role_data: UserUpdate, # Ожидаем {"role": "ADMIN"}
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_update = result.scalar_one_or_none()
    
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")
        
    if role_data.role:
        user_to_update.role = role_data.role
        
    await db.commit()
    await db.refresh(user_to_update)
    return user_to_update