from pydantic import BaseModel, StringConstraints
from typing import Annotated


class AccountCreate(BaseModel):
    account_type: str
    account_number: Annotated[str, StringConstraints(min_length=11)]
    balance: float | None = 0


class AccountDelete(BaseModel):
    account_number: Annotated[str, StringConstraints(min_length=11)]
