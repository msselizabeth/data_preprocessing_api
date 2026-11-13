import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncIterator

from .config import database_url

# from pathlib import Path

# database_path = Path(__file__).resolve().parent / "database_prod.db"

engine = create_async_engine(database_url)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session

# async def async_main() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     await engine.dispose()

# if __name__ == "__main__":
#     asyncio.run(async_main())