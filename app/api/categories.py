from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.category import get_categories, get_category_by_slug
from app.schemas.category import CategoryOut

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await get_categories(db)


@router.get("/{slug}/posts")
async def posts_by_category(slug: str, db: AsyncSession = Depends(get_db)):
    category = await get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(404, "Category not found")
    return category.posts
