from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..conexion_bd import obtener_bd
from ..modelos.facturas import Factura
from ..modelos.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionEditar,
    TransaccionRespuesta,
)

rutas_transacciones = APIRouter()


# ENDPOINTS DE TRANSACCIONES

@rutas_transacciones.get("/transacciones", response_model=list[TransaccionRespuesta])
def listar_transacciones(bd: Session = Depends(obtener_bd)):
    return bd.exec(select(Transaccion)).all()


@rutas_transacciones.get(
    "/transacciones/{transaccion_id}", response_model=TransaccionRespuesta
)
def listar_transaccion(transaccion_id: int, bd: Session = Depends(obtener_bd)):
    transaccion = bd.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    return transaccion


@rutas_transacciones.post(
    "/transacciones/{factura_id}", response_model=TransaccionRespuesta
)
def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear,
    bd: Session = Depends(obtener_bd),
):
    factura = bd.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe.",
        )
    transaccion = Transaccion.model_validate(
        datos_transaccion, update={"factura_id": factura_id}
    )
    bd.add(transaccion)
    bd.commit()
    bd.refresh(transaccion)
    return transaccion


@rutas_transacciones.patch(
    "/transacciones/{transaccion_id}", response_model=TransaccionRespuesta
)
def editar_transaccion(
    transaccion_id: int,
    datos_transaccion: TransaccionEditar,
    bd: Session = Depends(obtener_bd),
):
    transaccion = bd.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    transaccion.cantidad = datos_transaccion.cantidad
    transaccion.valor_unitario = datos_transaccion.valor_unitario
    bd.add(transaccion)
    bd.commit()
    bd.refresh(transaccion)
    return transaccion


@rutas_transacciones.delete(
    "/transacciones/{transaccion_id}", response_model=TransaccionRespuesta
)
def eliminar_transaccion(transaccion_id: int, bd: Session = Depends(obtener_bd)):
    transaccion = bd.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    bd.delete(transaccion)
    bd.commit()
    return transaccion
