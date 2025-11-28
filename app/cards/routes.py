from fastapi import APIRouter, Depends, HTTPException

from app.auth.infrastructure.dependencies import get_current_user

from app.cards.application.dto import CardCreateDto
from app.cards.application.services import CardService
from app.cards.domain.models import Card
from app.cards.infrastructure.repository import CardRepository
from app.cards.domain.exceptions import CardNotFound, UnauthorizedCardAccess

from app.core.database import get_db

from app.users.domain.models import User

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


@router.delete("/{card_number}")
async def delete(
    card_number: str,
    current_user: User = Depends(get_current_user),
    card_service: CardService = Depends(get_cards_service),
):
    try:
        card_service.delete_card(card_number, current_user.id)
    except CardNotFound:
        raise HTTPException(
            status_code=404, detail=f"La tarjeta {card_number} no existe"
        )
    except UnauthorizedCardAccess:
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar esta tarjeta"
        )

    return {"message": f"La tarjeta {card_number} se elimino exitosamente"}
