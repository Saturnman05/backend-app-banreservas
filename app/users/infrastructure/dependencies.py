from fastapi import Depends
from core.database import get_db
from .repository import UserRepository


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepository(db)
