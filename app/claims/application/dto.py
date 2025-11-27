from pydantic import BaseModel, StringConstraints
from typing import Annotated


class ClaimCreateDto(BaseModel):
    account_id: int
    card_id: int | None
    claim_description: str
    claim_type: Annotated[str, StringConstraints(max_length=200)]
