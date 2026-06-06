from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lista_clientes = []
lista_facturas = []
lista_transacciones = []

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None


class Factura(BaseModel):
    id: int
    fecha: str
    valor_total: float
    cliente: int

class Transaccion(BaseModel):
    id: int
    vr_unitario: float
    cantidad: int
    factura_id: int

@app.get("/clientes")
def listar_clientes(id: int = None):
    if id:
        for cliente in lista_clientes:
            if cliente.id == id:
                return {"Cliente": cliente}
    return {"Clientes": lista_clientes}

@app.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return {"Mensaje": "Cliente creado exitosamente"}


@app.put("/clientes")
def editar_cliente(datos_actualizados: Cliente, id: int = None):
    if id:
        for index, cliente in enumerate(lista_clientes):
            if cliente.id == id:
                lista_clientes[index] = datos_actualizados
                return {"Mensaje": "Cliente actualizado exitosamente"}
    return {"Mensaje": "No se encontró el cliente"}

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for index, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(index)
            return {"Mensaje": "Cliente eliminado exitosamente"}

@app.get("/facturas")
def listar_facturas(id: int = None):
    if id:
        for factura in lista_facturas:
            if factura.id == id:
                return {"Factura": factura}
    return {"Facturas": lista_facturas}

@app.post("/facturas")
def crear_factura(datos_factura: Factura):
    lista_facturas.append(datos_factura)
    return {"Mensaje": "Factura creada exitosamente"}

@app.put("/facturas")
def editar_factura(datos_actualizados: Factura, id: int = None):
    if id:
        for index, factura in enumerate(lista_facturas):
            if factura.id == id:
                lista_facturas[index] = datos_actualizados
                return {"Mensaje": "Factura actualizada exitosamente"}
    return {"Mensaje": "No se encontró la factura"}

@app.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for index, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(index)
            return {"Mensaje": "Factura eliminada exitosamente"}

@app.get("/transacciones")
def listar_transacciones(id: int = None):
    if id:
        for transaccion in lista_transacciones:
            if transaccion.id == id:
                return {"Transaccion": transaccion}
    return {"Transacciones": lista_transacciones}

@app.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):
    lista_transacciones.append(datos_transaccion)
    return {"Mensaje": "Transacción creada exitosamente"}

@app.put("/transacciones")
def editar_transaccion(datos_actualizados: Transaccion, id: int = None):
    if id:
        for index, transaccion in enumerate(lista_transacciones):
            if transaccion.id == id:
                lista_transacciones[index] = datos_actualizados
                return {"Mensaje": "Transacción actualizada exitosamente"}
    return {"Mensaje": "No se encontró la transacción"}

@app.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    for index, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones.pop(index)
            return {"Mensaje": "Transacción eliminada exitosamente"}