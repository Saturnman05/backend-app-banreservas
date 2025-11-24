from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_cards():
    return [
        {"id": 1, "card_number": "xxxx-xxxx-xxxx-xxxx"},
        {"id": 2, "card_number": "xxxx-xxxx-xxxx-xxxx"},
        {"id": 3, "card_number": "xxxx-xxxx-xxxx-xxxx"},
        {"id": 4, "card_number": "xxxx-xxxx-xxxx-xxxx"},
    ]
