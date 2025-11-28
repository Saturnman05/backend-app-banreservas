from fastapi import APIRouter, Depends, HTTPException

from auth.infrastructure.dependencies import get_current_user

from users.domain.models import User


router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name(),
        "phone": current_user.phone,
    }
