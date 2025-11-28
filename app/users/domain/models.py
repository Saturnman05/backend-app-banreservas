from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: str
    phone: str
    username: str
    hashed_password: str

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
