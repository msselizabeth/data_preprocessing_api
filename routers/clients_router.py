from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from db.api_clients_model import ApiClient
from schemas.api_client import ClientRegistrationResponse
from helpers.generate_api_key import generate_api_key

router = APIRouter()

@router.post("/clients", response_model=ClientRegistrationResponse, status_code=201)
async def register_client(
    session: AsyncSession = Depends(get_session),
) -> ClientRegistrationResponse:
    # Generate API Key
    key, key_hash = generate_api_key()

    #  Create a client
    client = ApiClient(api_key_hash=key_hash)
    session.add(client)
    await session.commit()

    return ClientRegistrationResponse(
        client_id=client.id, 
        api_key=key
    )
