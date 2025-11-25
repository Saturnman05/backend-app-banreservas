from fastapi import APIRouter, Depends, HTTPException
from .domain.exceptions import UserNotFound
from .infrastructure.dependencies import get_user_repository
from .infrastructure.repository import UserRepository

router = APIRouter()


@router.get("/")
async def list_users():
    return [
        {"id": 1, "user": "pepito"},
        {"id": 2, "user": "pepito"},
        {"id": 3, "user": "pepito"},
    ]


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, repo: UserRepository = Depends(get_user_repository)
):
    try:
        user = repo.get_by_id(user_id)
        return user
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
