from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.database.config import db_settings

engine = create_async_engine(
    url=db_settings.get_connection_string
)

async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)        

async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    async with async_session() as session:
        yield session
