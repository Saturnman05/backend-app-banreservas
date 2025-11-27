from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class CardDB(Base):
    __tablename__ = "tarjetas"

    id = Column("id_tarjeta", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        "id_usuario",
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
    )
    account_id = Column(
        "id_cuenta",
        Integer,
        ForeignKey("cuentas.id_cuenta"),
        nullable=True,
    )
    card_number = Column("numero_tarjeta", String(20), nullable=False)
    card_type = Column("tipo_tarjeta", String(20), nullable=False)

    usuario = relationship("UserDB", back_populates="tarjetas")
    cuenta = relationship("AccountDB", back_populates="tarjetas")
