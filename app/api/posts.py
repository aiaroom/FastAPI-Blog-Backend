from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.post import get_posts, get_post_by_slug
from app.schemas.post import PostOut

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])


@router.get("/", response_model=list[PostOut])
async def list_posts(db: AsyncSession = Depends(get_db)):
    return await get_posts(db)


@router.get("/{slug}", response_model=PostOut)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    post = await get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(404, "Post not found")
    return post
