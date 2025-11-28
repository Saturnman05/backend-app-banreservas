from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from app.core.database import Base


class ClaimDB(Base):
    __tablename__ = "reclamaciones"

    id = Column(
        "id_reclamacion", Integer, primary_key=True, index=True, autoincrement=True
    )
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
        nullable=False,
    )
    card_id = Column(
        "id_tarjeta",
        Integer,
        ForeignKey("tarjetas.id_tarjeta"),
        nullable=True,
    )
    claim_type = Column("motivo", String(200), nullable=False)
    description = Column("descripcion", Text, nullable=False)
    date_claim = Column(
        "fecha_reclamacion",
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    user = relationship("UserDB", back_populates="claims")
    account = relationship("AccountDB", back_populates="claim")
    card = relationship("CardDB", back_populates="claim")
