from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class UserDB(Base):
    __tablename__ = "usuarios"

    id = Column("id_usuario", Integer, primary_key=True, index=True)
    first_name = Column("nombre", String(50), nullable=False)
    last_name = Column("apellido", String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column("telefono", String(13), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    username = Column(String(100), nullable=False, unique=True)

    # Relaciones
    # cuentas = relationship("cuenta", back_populates="usuario")
    # tarjetas = relationship("tarjeta", back_populates="usuario")
    # reclamaciones = relationship("reclamacion", back_populates="usuario")
