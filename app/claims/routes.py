from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_claims():
    return [
        {"id": 1, "motivo": "me robaron"},
        {"id": 2, "motivo": "me robaron"},
        {"id": 3, "motivo": "me robaron"},
    ]
