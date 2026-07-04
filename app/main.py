from fastapi import FastAPI
from .conexion_bd import Base, engine
from .modelos import clientes, facturas, transacciones  # noqa: F401 (necesarios para crear las tablas)
from .enrutadores.clientes import rutas_clientes
from .enrutadores.facturas import rutas_facturas
from .enrutadores.transacciones import rutas_transacciones

# Crea las tablas en el archivo .sqlite3 si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Facturación - Clientes (con Base de Datos)")

app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])
