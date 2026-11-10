import secrets

from pydantic import JsonValue
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.json_mappings_model import JsonMapping
from helpers.json_masking import mask_json, restore_json
from helpers.json_validator import validate_restore_data


async def create_json_mappings(
    data: dict[str, JsonValue], paths: list[str], client_id: int, session: AsyncSession
) -> tuple[dict[str, JsonValue], str]:

    masked_data, mappings, field_placeholders = mask_json(data, paths)

    if not mappings:
        raise ValueError("No non-empty values to mask.")

    # Save mapppings in DB
    new_token = secrets.token_urlsafe(32)
    new_mapping = JsonMapping(
        token=new_token,
        client_id=client_id,
        mapping=mappings,
        field_placeholders=field_placeholders,
    )
    session.add(new_mapping)
    await session.commit()

    return (masked_data, new_token)


async def restore_json_mappings(
    data: dict[str, JsonValue],
    token: str,
    session: AsyncSession,
    client_id: int,
    partial: bool = False,
) -> dict[str, JsonValue]:
    statement = select(JsonMapping).where(
        JsonMapping.token == token, JsonMapping.client_id == client_id
    )
    res = await session.execute(statement)
    record = res.scalar_one_or_none()
    if record is None:
        raise LookupError("Mapping not found.")

    validate_restore_data(
        data=data, field_placeholders=record.field_placeholders, partial=partial
    )

    restored_data = restore_json(data, record.mapping)

    if not partial:
        await session.delete(record)
        await session.commit()

    return restored_data
