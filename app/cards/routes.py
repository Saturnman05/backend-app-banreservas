from fastapi import APIRouter, Depends

from auth.infrastructure.dependencies import get_current_user

from cards.application.services import CardService
from cards.infrastructure.repository import CardRepository

from core.database import get_db

from users.domain.models import User

router = APIRouter()


def get_cards_service(db=Depends(get_db)):
    repo = CardRepository(db)
    return CardService(repo)


@router.get("/")
async def list_cards(
    current_user: User = Depends(get_current_user),
    card_service: CardService = Depends(get_cards_service),
):
    cards = card_service.get_cards_by_user(current_user.id)
    return cards
