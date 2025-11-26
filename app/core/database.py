from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Conexión a la base de datos en la nube
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Evita errores si la conexión está inactiva
)

# Crea sesiones para los requests
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

# Base para los modelos ORM
Base = declarative_base()


# Dependencia para inyectar la BD en los endpoints o servicios
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
