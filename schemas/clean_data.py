from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone


class CleanDataRequest(BaseModel):
    text: str
    additional_values: list[str] = Field(default_factory=list)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be blank.")
        return value

    @field_validator("additional_values")
    @classmethod
    def reject_blank_additional_values(cls, value: list[str]) -> list[str]:
        for i, val in enumerate(value):
            if not val.strip():
                raise ValueError(f"additional_values[{i}] must not be blank.")
        return value
