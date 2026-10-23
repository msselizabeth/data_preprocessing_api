from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_session
from db.api_clients_model import ApiClient
from schemas.api_client import ClientRegistrationResponse
from helpers.generate_api_key import generate_api_key

app = FastAPI()


@app.get("/health")
async def heath_check():
    return {"status": "ok", "message": "Hello from Data Proccessing API !"}


@app.post("/clients", response_model=ClientRegistrationResponse, status_code=201)
async def register_client(
    session: AsyncSession = Depends(get_session),
) -> ClientRegistrationResponse:
    key, key_hash = generate_api_key()
    client = ApiClient(api_key_hash=key_hash)
    session.add(client)
    await session.commit()
    return ClientRegistrationResponse(client_id=client.id, api_key=key)
