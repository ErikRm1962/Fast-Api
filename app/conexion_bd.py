from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Archivo de base de datos SQLite
URL_BASE_DATOS = "sqlite:///./bd_facturacion.sqlite3"

engine = create_engine(
    URL_BASE_DATOS, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obtener_bd():
    """Dependencia de FastAPI: entrega una sesión de BD y la cierra al terminar."""
    bd = SessionLocal()
    try:
        yield bd
    finally:
        bd.close()
