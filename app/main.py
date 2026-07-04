from fastapi import FastAPI
from .enrutadores.clientes import rutas_clientes
from .enrutadores.facturas import rutas_facturas
from .enrutadores.transacciones import rutas_transacciones

app = FastAPI(title="API Facturación - Clientes")

# Incluir rutas
app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])
