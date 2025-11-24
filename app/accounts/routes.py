from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_accounts():
    return [{"id": 1, "balance": 1000000}]
