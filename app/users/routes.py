from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def list_users():
    return [
        {"id": 1, "user": "pepito"},
        {"id": 2, "user": "pepito"},
        {"id": 3, "user": "pepito"},
    ]
