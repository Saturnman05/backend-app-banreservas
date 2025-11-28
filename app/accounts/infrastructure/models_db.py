from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class AccountDB(Base):
    __tablename__ = "cuentas"

    id = Column("id_cuenta", Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        "id_usuario",
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
    )

    account_number = Column("numero_cuenta", String(11), nullable=False)
    account_type = Column("tipo_cuenta", String(20), nullable=False)
    balance = Column("saldo", DECIMAL(18, 2), nullable=False)

    usuario = relationship("UserDB", back_populates="cuentas")
    tarjetas = relationship("CardDB", back_populates="cuenta")
    claim = relationship("ClaimDB", back_populates="account")
