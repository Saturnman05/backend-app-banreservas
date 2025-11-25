from pydantic import BaseModel, EmailStr, constr


class UserRegisterDTO(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    email: EmailStr
    phone: constr(min_length=7, max_length=13)
    username: constr(min_length=3)
    password: constr(min_length=6)
