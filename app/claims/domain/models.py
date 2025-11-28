from pydantic import BaseModel


class Claim(BaseModel):
    id: int | None
    user_id: int
    account_id: int
    card_id: int | None
    claim_type: str
    claim_description: str
