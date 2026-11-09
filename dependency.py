#to yield an isolated database session per HTTP request and cleanly close it when it finished
from database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Ensuring if a database exception occurs , session.rollback() triggers to prevent uncommitted dirty data states.