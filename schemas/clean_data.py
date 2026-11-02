from pydantic import BaseModel, Field, field_validator


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
    def normalize_additional_values(cls, value: list[str]) -> list[str]:
        cleaned_values = []

        for i, val in enumerate(value):
            cleaned = val.strip()
            if not cleaned:
                raise ValueError(f"additional_values[{i}] must not be blank.")
            cleaned_values.append(cleaned)
        return cleaned_values
