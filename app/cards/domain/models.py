from pydantic import BaseModel


class Card(BaseModel):
    id: int
    user_id: int
    account_id: int | None
    card_number: str
    card_type: str
