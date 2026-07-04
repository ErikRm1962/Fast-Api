from fastapi import APIRouter, HTTPException, status
from ..modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from ..listas import lista_facturas, lista_transacciones

rutas_transacciones = APIRouter()


# ENDPOINTS DE TRANSACCIONES

# Listar todas las transacciones
@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return lista_transacciones


# Listar una sola transaccion
@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def listar_transaccion(transaccion_id: int):
    for obj_transaccion in lista_transacciones:
        if obj_transaccion.id == transaccion_id:
            return obj_transaccion
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La transacción con id {transaccion_id}, no existe",
    )


# Crear transacción (asociada a una factura)
@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    # buscar factura
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura

    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe.",
        )

    transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_val.factura_id = factura_id
    transaccion_val.id = len(lista_transacciones) + 1

    factura_encontrada.transacciones.append(transaccion_val)
    lista_transacciones.append(transaccion_val)

    return transaccion_val


# Editar transacción
@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionEditar):
    for transaccion in lista_transacciones:
        if transaccion.id == transaccion_id:
            transaccion.cantidad = datos_transaccion.cantidad
            transaccion.valor_unitario = datos_transaccion.valor_unitario
            return transaccion
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La transacción con id {transaccion_id}, no existe",
    )


# Eliminar transacción
@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int):
    for i, transaccion in enumerate(lista_transacciones):
        if transaccion.id == transaccion_id:
            transaccion_eliminada = lista_transacciones.pop(i)
            # también la quitamos de la lista de la factura correspondiente
            for factura in lista_facturas:
                if factura.id == transaccion_eliminada.factura_id:
                    factura.transacciones = [
                        t for t in factura.transacciones if t.id != transaccion_id
                    ]
            return transaccion_eliminada
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"La transacción con id {transaccion_id}, no existe",
    )
