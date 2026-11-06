from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from db.api_clients_model import ApiClient
from db.json_mappings_model import JsonMapping
from schemas.clean_json import CleanJsonRequest, CleanJsonResponse
from helpers.json_masking import mask_json, restore_json
from services.json_masking import create_json_mappings
from auth import get_current_client

router = APIRouter()


@router.post("/json/mask", response_model=CleanJsonResponse)
async def json_mask(
    body: CleanJsonRequest,
    client: ApiClient = Depends(get_current_client),
    session: AsyncSession = Depends(get_session),
) -> CleanJsonResponse:

    try:
        masked_data, token = await create_json_mappings(
            data=body.data, paths=body.paths, client_id=client.id, session=session
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return CleanJsonResponse(data=masked_data, token=token)
