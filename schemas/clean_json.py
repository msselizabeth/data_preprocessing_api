from pydantic import BaseModel, JsonValue, Field, field_validator


class CleanJsonRequest(BaseModel):
    data: dict[str, JsonValue]
    paths: list[str] = Field(min_length=1)

    @field_validator("paths")
    @classmethod
    def reject_invalid(cls, value: list[str]) -> list[str]:
        for i, v in enumerate(value):
            if v == "":
                raise ValueError(f"Empty values are not valid. Please remove or provide a value at index: {i}.")

            if not v.startswith("/"):
                raise ValueError(f"Invalid path at index: {i}. Should start from '/'." )

            if v.strip() == "/":
                 raise ValueError(f"Invalid path at index: {i}. Please provide a filed name after '/'." )

        return value

class CleanJsonResponse(BaseModel):
    data: dict[str, JsonValue]
    token: str

class RestoreJsonRequest(BaseModel):
    data: dict[str, JsonValue]
    token: str = Field(min_length=1)

class RestoreJsonResponse(BaseModel):
    data: dict[str, JsonValue]

