from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class CardBD(Base):
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

    user = relationship("UserDB", back_populates="tarjetas")
    account = relationship("AccountDB", back_populates="cuentas")
