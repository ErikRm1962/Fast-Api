from sqlmodel import SQLModel, create_engine, Session

# Archivo de base de datos SQLite
URL_BASE_DATOS = "sqlite:///./bd_facturacion.sqlite3"

engine = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})


def crear_bd_y_tablas():
    """Crea el archivo .sqlite3 y las tablas si no existen."""
    SQLModel.metadata.create_all(engine)


def obtener_bd():
    """Dependencia de FastAPI: entrega una sesion de BD y la cierra al terminar."""
    with Session(engine) as session:
        yield session
