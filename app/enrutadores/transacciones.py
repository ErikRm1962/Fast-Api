from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..conexion_bd import obtener_bd
from ..modelos.facturas import FacturaBD
from ..modelos.transacciones import TransaccionBD
from ..esquemas.transacciones import Transaccion, TransaccionCrear, TransaccionEditar

rutas_transacciones = APIRouter()


# ENDPOINTS DE TRANSACCIONES

@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(bd: Session = Depends(obtener_bd)):
    return bd.query(TransaccionBD).all()


@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transaccion)
async def listar_transaccion(transaccion_id: int, bd: Session = Depends(obtener_bd)):
    transaccion = (
        bd.query(TransaccionBD).filter(TransaccionBD.id == transaccion_id).first()
    )
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    return transaccion


@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear,
    bd: Session = Depends(obtener_bd),
):
    factura = bd.query(FacturaBD).filter(FacturaBD.id == factura_id).first()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe.",
        )
    transaccion_bd = TransaccionBD(
        **datos_transaccion.model_dump(), factura_id=factura_id
    )
    bd.add(transaccion_bd)
    bd.commit()
    bd.refresh(transaccion_bd)
    return transaccion_bd


@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transaccion)
async def editar_transaccion(
    transaccion_id: int,
    datos_transaccion: TransaccionEditar,
    bd: Session = Depends(obtener_bd),
):
    transaccion_bd = (
        bd.query(TransaccionBD).filter(TransaccionBD.id == transaccion_id).first()
    )
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    transaccion_bd.cantidad = datos_transaccion.cantidad
    transaccion_bd.valor_unitario = datos_transaccion.valor_unitario
    bd.commit()
    bd.refresh(transaccion_bd)
    return transaccion_bd


@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transaccion)
async def eliminar_transaccion(transaccion_id: int, bd: Session = Depends(obtener_bd)):
    transaccion_bd = (
        bd.query(TransaccionBD).filter(TransaccionBD.id == transaccion_id).first()
    )
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La transacción con id {transaccion_id}, no existe",
        )
    bd.delete(transaccion_bd)
    bd.commit()
    return transaccion_bd
