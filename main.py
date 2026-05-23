from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lista_clientes = []

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None


@app.get("/clientes")
def listar_clientes():
    return {"Clientes": lista_clientes}


@app.get("/clientes/{id}")
def listar_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return {"Cliente": cliente}


@app.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return {"Mensaje": "Cliente creado exitosamente"}


@app.put("/clientes/{id}")
def editar_cliente(id: int, datos_actualizados: Cliente):
    for index, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes[index] = datos_actualizados
            return {"Mensaje": "Cliente actualizado exitosamente"}


@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for index, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(index)
            return {"Mensaje": "Cliente eliminado exitosamente"}