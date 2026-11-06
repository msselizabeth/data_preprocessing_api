import secrets

from pydantic import JsonValue
from sqlalchemy.ext.asyncio import AsyncSession

from db.json_mappings_model import JsonMapping
from helpers.json_masking import mask_json, restore_json


async def create_json_mappings(
    data: dict[str, JsonValue], paths: list[str], client_id: int, session: AsyncSession
) -> tuple[dict[str, JsonValue], StopAsyncIteration]:

    masked_data, mappings = mask_json(data, paths)

    # Save mapppings in DB
    new_token = secrets.token_urlsafe(32)
    new_mapping = JsonMapping(token=new_token, client_id=client_id, mapping=mappings)
    session.add(new_mapping)
    await session.commit()

    return (masked_data, new_token)
