from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta de la base de datos SQLite (se guardará como archivo local tasks.db)
DATABASE_URL = "sqlite:///./tasks.db"

# Crea la conexión principal con la base de datos
engine = create_engine(
    DATABASE_URL,

    # Necesario en SQLite para evitar problemas de hilos con FastAPI
    connect_args={"check_same_thread":False}
)

# Crea sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base común desde la que heredarán los modelos/tablas
Base = declarative_base()