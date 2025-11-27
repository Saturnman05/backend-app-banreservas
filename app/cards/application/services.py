from cards.domain.models import Card
from cards.infrastructure.repository import CardRepository


class CardService:
    def __init__(self, repo: CardRepository):
        self.repo = repo

    def create_card(self, card: Card) -> Card:
        card = self.repo.get_by_number(card.card_number)

        return self.repo.create(card)

    def get_cards_by_user(self, user_id: int) -> list[Card]:
        cards: list[Card] = self.repo.list_all_by_user_id(user_id)
        return cards
