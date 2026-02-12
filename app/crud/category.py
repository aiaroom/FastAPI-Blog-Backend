from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category import Category


async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(Category).where(Category.slug == slug))
    return result.scalar_one_or_none()


async def create_category(db: AsyncSession, name: str, slug: str):
    category = Category(name=name, slug=slug)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
