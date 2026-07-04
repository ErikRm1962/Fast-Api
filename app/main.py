from fastapi import FastAPI
from .conexion_bd import crear_bd_y_tablas
from .enrutadores.clientes import rutas_clientes
from .enrutadores.facturas import rutas_facturas
from .enrutadores.transacciones import rutas_transacciones

app = FastAPI(title="API Facturación - Clientes (SQLModel)")


@app.on_event("startup")
def iniciar_bd():
    # Crea el archivo .sqlite3 y las tablas si no existen
    crear_bd_y_tablas()


app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])
