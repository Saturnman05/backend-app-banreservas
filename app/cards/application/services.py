from app.cards.domain.models import Card
from app.cards.infrastructure.repository import CardRepository
from app.cards.domain.exceptions import CardNotFound, UnauthorizedCardAccess


class CardService:
    def __init__(self, repo: CardRepository):
        self.repo = repo

    def create_card(self, card: Card) -> Card:
        return self.repo.create(card)

    def get_cards_by_user(self, user_id: int) -> list[Card]:
        cards: list[Card] = self.repo.list_all_by_user_id(user_id)
        return cards

    def get_card_by_number(self, card_number: str) -> Card:
        return self.repo.get_by_number(card_number=card_number)

    def delete_card(self, card_number: str, user_id: int):
        card = self.get_card_by_number(card_number)
        if card == None:
            raise CardNotFound()

        if card.user_id != user_id:
            raise UnauthorizedCardAccess()

        self.repo.delete(card.id)
