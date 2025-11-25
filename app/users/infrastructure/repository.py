from sqlalchemy.orm import Session
from users.infrastructure.models_db import UserDB
from users.domain.models import User
from users.domain.exceptions import UserNotFound


class UserRepository:
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

    def to_domain(self, user_db: UserDB) -> User:
        """Convierte UserDB → User (dominio)."""
        return User(
            id=user_db.id,
            first_name=user_db.first_name,
            last_name=user_db.last_name,
            email=user_db.email,
            phone=user_db.phone_number,  # dominio tiene otro nombre
            username=user_db.username,
            hashed_password=user_db.hashed_password,
        )

    def to_db(self, user: User) -> UserDB:
        """Convierte User (dominio) → UserDB."""
        return UserDB(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone,  # distinto nombre pero mapeado
            username=user.username,
            hashed_password=user.hashed_password,
        )

    # ----------------------------
    #   CRUD
    # ----------------------------

    def create(self, user: User) -> User:
        obj = self.to_db(user)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def get_by_id(self, id: int) -> User:
        obj = self.db.query(UserDB).filter(UserDB.id == id).first()
        if not obj:
            raise UserNotFound(f"User with id={id} not found")
        return self.to_domain(obj)

    def get_by_email(self, email: str) -> User:
        obj = self.db.query(UserDB).filter(UserDB.email == email).first()
        if not obj:
            raise UserNotFound(f"User with email {email} not found")
        return self.to_domain(obj)

    def list_all(self) -> list[User]:
        records = self.db.query(UserDB).all()
        return [self.to_domain(r) for r in records]

    def update(self, id: int, **fields) -> User:
        obj = self.db.query(UserDB).filter(UserDB.id == id).first()
        if not obj:
            raise UserNotFound(f"User with id={id} not found")

        for key, value in fields.items():
            # evita campos inexistentes
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return self.to_domain(obj)

    def delete(self, id: int) -> None:
        obj = self.db.query(UserDB).filter(UserDB.id == id).first()
        if not obj:
            raise UserNotFound(f"User with id={id} not found")

        self.db.delete(obj)
        self.db.commit()
