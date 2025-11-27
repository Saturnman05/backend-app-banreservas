from fastapi import APIRouter, Depends, HTTPException

from auth.infrastructure.dependencies import get_current_user

from cards.application.dto import CardCreateDto
from cards.application.services import CardService
from cards.domain.models import Card
from cards.infrastructure.repository import CardRepository
from cards.domain.exceptions import CardNotFound

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


@router.post("/")
async def create_card(
    data: CardCreateDto,
    current_user: User = Depends(get_current_user),
    card_service: CardService = Depends(get_cards_service),
):
    try:
        if card_service.get_card_by_number(data.card_number):
            raise HTTPException(400, "Ya existe una tarjeta con ese número")
    except CardNotFound:
        pass

    card = Card(
        id=None,
        user_id=current_user.id,
        account_id=data.account_id,
        card_number=data.card_number,
        card_type=data.card_type,
    )

    card = card_service.create_card(card)

    return {
        "message": "Tarjeta creada exitosamente",
        "card": {
            "id": card.id,
            "card_number": card.card_number,
            "card_type": card.card_type,
        },
    }
