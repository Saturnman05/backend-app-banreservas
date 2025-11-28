from sqlalchemy.orm import Session

from app.cards.domain.models import Card
from app.cards.domain.exceptions import CardNotFound
from app.cards.infrastructure.models_db import CardDB


class CardRepository:
    """
    Repositorio de tarjetas.
    Capa de infraestructura: depende de SQLAlchemy.
    Maneja conversiones entre el modelo ORM y el modelo de dominio.
    """

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------
    #   CONVERSIONES
    # ----------------------------

    def to_domain(self, card_db: CardDB) -> Card:
        """Convierte CardDB → Card (dominio)."""
        return Card(
            id=card_db.id,
            card_number=card_db.card_number,
            card_type=card_db.card_type,
            user_id=card_db.user_id,
            account_id=card_db.account_id,
        )

    def to_db(self, card: Card) -> CardDB:
        """Convierte Card (dominio) → CardDB."""
        return CardDB(
            id=card.id,
            card_number=card.card_number,
            card_type=card.card_type,
            user_id=card.user_id,
            account_id=card.account_id,
        )

    # ----------------------------
    #   CRUD
    # ----------------------------

    def create(self, Card: Card) -> Card:
        obj = self.to_db(Card)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def get_by_id(self, id: int) -> Card:
        obj = self.db.query(CardDB).filter(CardDB.id == id).first()
        if not obj:
            raise CardNotFound(f"Card with id={id} not found")
        return self.to_domain(obj)

    def get_by_number(self, card_number: str) -> Card:
        obj = self.db.query(CardDB).filter(CardDB.card_number == card_number).first()
        if not obj:
            raise CardNotFound(f"Card with card_number={card_number} not found")
        return self.to_domain(obj)

    def list_all(self) -> list[Card]:
        records = self.db.query(CardDB).all()
        return [self.to_domain(r) for r in records]

    def list_all_by_user_id(self, user_id: int) -> list[Card]:
        records: list[CardDB] = self.db.query(CardDB).filter(CardDB.user_id == user_id)
        return [self.to_domain(r) for r in records]

    def update(self, id: int, **fields) -> Card:
        obj = self.db.query(CardDB).filter(CardDB.id == id).first()
        if not obj:
            raise CardNotFound(f"Card with id={id} not found")

        for key, value in fields.items():
            # evita campos inexistentes
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def delete(self, id: int) -> None:
        obj = self.db.query(CardDB).filter(CardDB.id == id).first()
        if not obj:
            raise CardNotFound(f"Card with id={id} not found")

        self.db.delete(obj)
        self.db.commit()
