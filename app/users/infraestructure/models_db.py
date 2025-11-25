from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column("id_cuenta", Integer, primary_key=True, index=True)
    first_name = Column("nombre", String(50), nullable=False)
    last_name = Column("apellido", String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column("telefono", String(13), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    username = Column(String(100), nullable=False, unique=True)

    # Relaciones
    cuentas = relationship("Cuenta", back_populates="usuario")
    tarjetas = relationship("Tarjeta", back_populates="usuario")
    reclamaciones = relationship("Reclamacion", back_populates="usuario")
