from sqlalchemy.orm import Session

from claims.domain.models import Claim
from claims.domain.exceptions import ClaimNotFound
from claims.infrastructure.models_db import ClaimDB


class ClaimRepository:
    """
    Repositorio de reclamaciones.
    Capa de infraestructura: depende de SQLAlchemy.
    Maneja conversiones entre el modelo ORM y el modelo de dominio.
    """

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------
    #   CONVERSIONES
    # ----------------------------

    def to_domain(self, claim_db: ClaimDB) -> Claim:
        """Convierte ClaimDB → Claim (dominio)."""
        return Claim(
            id=claim_db.id,
            user_id=claim_db.user_id,
            account_id=claim_db.account_id,
            card_id=claim_db.card_id,
            claim_description=claim_db.description,
            claim_type=claim_db.claim_type,
        )

    def to_db(self, claim: Claim) -> ClaimDB:
        """Convierte Claim (dominio) → ClaimDB."""
        return ClaimDB(
            id=claim.id,
            user_id=claim.user_id,
            account_id=claim.account_id,
            card_id=claim.card_id,
            description=claim.claim_description,
            claim_type=claim.claim_type,
        )

    # ----------------------------
    #   CRUD
    # ----------------------------

    def create(self, claim: Claim) -> Claim:
        obj = self.to_db(claim)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def get_by_id(self, id: int) -> Claim:
        obj = self.db.query(ClaimDB).filter(ClaimDB.id == id).first()
        if not obj:
            raise ClaimNotFound(f"Claim with id={id} not found")
        return self.to_domain(obj)

    def list_all(self) -> list[Claim]:
        records = self.db.query(ClaimDB).all()
        return [self.to_domain(r) for r in records]

    def list_by_account(self, account_id: int) -> list[Claim]:
        records: list[ClaimDB] = self.db.query(ClaimDB).filter(
            ClaimDB.account_id == account_id
        )
        return [self.to_domain(r) for r in records]

    def list_by_card(self, card_id: int) -> list[Claim]:
        records: list[ClaimDB] = self.db.query(ClaimDB).filter(
            ClaimDB.card_id == card_id
        )
        return [self.to_domain(r) for r in records]

    def list_all_by_user_id(self, user_id: int) -> list[Claim]:
        records: list[ClaimDB] = self.db.query(ClaimDB).filter(
            ClaimDB.user_id == user_id
        )
        return [self.to_domain(r) for r in records]

    def update(self, id: int, **fields) -> Claim:
        obj = self.db.query(ClaimDB).filter(ClaimDB.id == id).first()
        if not obj:
            raise ClaimNotFound(f"Claim with id={id} not found")

        for key, value in fields.items():
            # evita campos inexistentes
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def delete(self, id: int) -> None:
        obj = self.db.query(ClaimDB).filter(ClaimDB.id == id).first()
        if not obj:
            raise ClaimNotFound(f"Claim with id={id} not found")

        self.db.delete(obj)
        self.db.commit()
