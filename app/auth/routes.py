from fastapi import APIRouter
from .domain.models import UserLogin

router = APIRouter()


@router.post("/login/")
async def login(user: UserLogin):
    return {
        "email": user.email,
        "password": user.password,
    }
