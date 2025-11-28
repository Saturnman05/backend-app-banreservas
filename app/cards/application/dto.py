from pydantic import BaseModel, StringConstraints
from typing import Annotated


class CardCreateDto(BaseModel):
    account_id: int | None
    card_number: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=16, max_length=20)
    ]
    card_type: Annotated[str, StringConstraints(max_length=20)]
