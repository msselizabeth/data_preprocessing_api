from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_session
from db.api_clients_model import ApiClient
import hashlib
from sqlalchemy import select


header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


async def read_header(key: str | None = Depends(header_scheme)) -> str:
    if key is None or key == "":
        raise HTTPException(status_code=401, detail="Missing API Key")
        
    return key

async def get_current_client(key: str = Depends(read_header), session: AsyncSession = Depends(get_session)) -> ApiClient:
    key_hash = hashlib.sha256(key.encode('utf-8'), usedforsecurity=True).hexdigest()
    statement = select(ApiClient).where(ApiClient.api_key_hash == key_hash)
    res = await session.execute(statement)
    client = res.scalar_one_or_none()
    if client is None or not client.is_active:
        raise HTTPException(status_code=401, detail="Invalid Api Key")
    return client
