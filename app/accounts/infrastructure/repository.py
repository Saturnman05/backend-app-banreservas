from sqlalchemy.orm import Session
from accounts.infrastructure.models_db import AccountDB
from accounts.domain.models import Account
from accounts.domain.exceptions import AccountNotFound


class AccountRepository:
    """
    Repositorio de usuarios.
    Capa de infraestructura: depende de SQLAlchemy.
    Maneja conversiones entre el modelo ORM y el modelo de dominio.
    """

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------
    #   CONVERSIONES
    # ----------------------------

    def to_domain(self, account_db: AccountDB) -> Account:
        """Convierte AccountDB → User (dominio)."""
        return Account(
            id=account_db.id,
            account_number=account_db.account_number,
            account_type=account_db.account_type,
            balance=account_db.balance,
            user_id=account_db.user_id,
        )

    def to_db(self, account: Account) -> AccountDB:
        """Convierte User (dominio) → AccountDB."""
        return AccountDB(
            id=account.id,
            account_number=account.account_number,
            account_type=account.account_type,
            balance=account.balance,
            user_id=account.user_id,
        )

    # ----------------------------
    #   CRUD
    # ----------------------------

    def create(self, account: Account) -> Account:
        obj = self.to_db(account)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def get_by_id(self, id: int) -> Account:
        obj = self.db.query(AccountDB).filter(AccountDB.id == id).first()
        if not obj:
            raise AccountNotFound(f"User with id={id} not found")
        return self.to_domain(obj)

    def list_all(self) -> list[Account]:
        records = self.db.query(AccountDB).all()
        return [self.to_domain(r) for r in records]

    def list_all_by_user_id(self, user_id: int) -> list[Account]:
        records: list[AccountDB] = self.db.query(AccountDB).filter(
            AccountDB.user_id == user_id
        )
        return [self.to_domain(r) for r in records]

    def update(self, id: int, **fields) -> Account:
        obj = self.db.query(AccountDB).filter(AccountDB.id == id).first()
        if not obj:
            raise AccountNotFound(f"User with id={id} not found")

        for key, value in fields.items():
            # evita campos inexistentes
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def delete(self, id: int) -> None:
        obj = self.db.query(AccountDB).filter(AccountDB.id == id).first()
        if not obj:
            raise AccountNotFound(f"User with id={id} not found")

        self.db.delete(obj)
        self.db.commit()
