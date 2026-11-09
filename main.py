from fastapi import FastAPI, Depends, HTTPException

from db.api_clients_model import ApiClient
from auth import get_current_client

from routers.clients_router import router as clients_router
from routers.json_masking_router import router as json_masking_router


app = FastAPI()

app.include_router(clients_router)
app.include_router(json_masking_router)


@app.get("/health")
async def heath_check():
    return {"status": "ok", "message": "Hello from Data Proccessing API !"}


@app.get("/auth-check", status_code=200)
async def auth_check(client: ApiClient = Depends(get_current_client)) -> dict:
    return {"client_id": client.id}
