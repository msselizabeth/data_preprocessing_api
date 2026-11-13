import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncIterator

from .api_clients_model import Base
from .json_mappings_model import JsonMapping
from .config import database_url

# from pathlib import Path

# database_path = Path(__file__).resolve().parent / "database_prod.db"

engine = create_async_engine(f"sqlite+aiosqlite:///{database_url}")
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