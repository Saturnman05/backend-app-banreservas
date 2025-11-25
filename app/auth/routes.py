from fastapi import APIRouter, Depends
from .domain.models import UserLogin
from sqlalchemy.orm import Session
from core.database import get_db


router = APIRouter()


@router.post("/login")
async def login(user: UserLogin):
    return {
        "email": user.email,
        "password": user.password,
    }


@router.post("/signup")
async def signup(db: Session = Depends(get_db)):
    return db.query()
