from fastapi import APIRouter, Depends, HTTPException
from .domain.exceptions import UserNotFound
from .infrastructure.dependencies import get_user_repository
from .infrastructure.repository import UserRepository

router = APIRouter()


@router.get("/")
async def list_users(repo: UserRepository = Depends(get_user_repository)):
    try:
        users = repo.list_all()
        return users
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, repo: UserRepository = Depends(get_user_repository)
):
    try:
        user = repo.get_by_id(user_id)
        return user
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
