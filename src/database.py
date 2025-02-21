from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config_data.config import Config, load_config

settings: Config = load_config(".env")
database_config = settings.database
DATABASE_URL = database_config.DATABASE_URL

# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def clear_tables():
    async with async_session() as session:
        await session.execute(text("DELETE FROM users"))
        await session.commit()


class Base(AsyncAttrs, DeclarativeBase):
    pass
