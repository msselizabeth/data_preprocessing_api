from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from db.api_clients_model import ApiClient
from schemas.clean_json import (
    CleanJsonRequest,
    CleanJsonResponse,
    RestoreJsonRequest,
    RestoreJsonResponse,
)
from services.json_masking import create_json_mappings, restore_json_mappings
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


@router.post("/json/restore", response_model=RestoreJsonResponse)
async def json_restore(
    body: RestoreJsonRequest,
    client: ApiClient = Depends(get_current_client),
    session: AsyncSession = Depends(get_session),
) -> RestoreJsonResponse:

    try:
        restored_data = await restore_json_mappings(
            data=body.data,
            token=body.token,
            partial=body.partial,
            client_id=client.id,
            session=session,
        )
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return RestoreJsonResponse(data=restored_data)
