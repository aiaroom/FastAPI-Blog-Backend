from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.database import Base
from app.models import user, post, category
from app.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        # Определяем синхронную функцию, которая примет соединение
        def do_run_migrations_sync(connection):
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            
            with context.begin_transaction():
                context.run_migrations()

        async with connectable.connect() as connection:
            # Передаем одну функцию, которая все сделает
            await connection.run_sync(do_run_migrations_sync)

    import asyncio
    asyncio.run(do_run_migrations())


run_migrations_online()
