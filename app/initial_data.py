import asyncio
import logging
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.security.hashing import hash_password

ADMIN_EMAIL = "admin@blog.com"
ADMIN_PASSWORD = "admin"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_initial_data():
    async with AsyncSessionLocal() as session:
        logger.info("Checking for admin user...")
        
        result = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
        user = result.scalar_one_or_none()
        
        if user:
            logger.info(f"Admin user {ADMIN_EMAIL} already exists.")
        else:
            logger.info(f"Creating admin user {ADMIN_EMAIL}...")
            new_admin = User(
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True
            )
            session.add(new_admin)
            await session.commit()
            logger.info("Admin user created successfully!")

if __name__ == "__main__":
    asyncio.run(create_initial_data())