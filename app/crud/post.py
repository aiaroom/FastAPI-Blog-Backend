from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.post import Post


async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()


async def get_post_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(select(Post).where(Post.slug == slug))
    return result.scalar_one_or_none()


async def create_post(db: AsyncSession, **kwargs):
    post = Post(**kwargs)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
