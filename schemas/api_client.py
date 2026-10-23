from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone


class ClientRegistrationResponse(BaseModel):
    client_id: int
    api_key: str

    # model_config = ConfigDict()  # custom confuguration