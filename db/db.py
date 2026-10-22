import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from api_clients_model import Base

engine = create_async_engine("sqlite+aiosqlite:///database_prod.db", echo=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())