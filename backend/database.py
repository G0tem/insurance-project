from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER
from sqlalchemy.orm import declarative_base


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_async_session():
    async with async_session() as session:
        yield session