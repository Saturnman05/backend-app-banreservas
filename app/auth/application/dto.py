from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated


class UserRegisterDTO(BaseModel):
    first_name: Annotated[str, StringConstraints(min_length=1)]
    last_name: Annotated[str, StringConstraints(min_length=1)]
    email: EmailStr
    phone: Annotated[str, StringConstraints(min_length=7, max_length=13)]
    username: Annotated[str, StringConstraints(min_length=3)]
    password: Annotated[str, StringConstraints(min_length=6)]
