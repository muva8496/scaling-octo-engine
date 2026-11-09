# database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Bringing in postgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:8496@localhost:5432/Quickmart_SQLAlchemy"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Configure the async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for your SQLAlchemy models
class Base(DeclarativeBase):
    pass