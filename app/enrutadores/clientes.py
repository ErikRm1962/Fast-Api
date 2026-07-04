from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..conexion_bd import obtener_bd
from ..modelos.clientes import ClienteBD
from ..esquemas.clientes import Cliente, ClienteCrear, ClienteEditar

rutas_clientes = APIRouter()


# ENDPOINTS DE CLIENTES

@rutas_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(bd: Session = Depends(obtener_bd)):
    return bd.query(ClienteBD).all()


@rutas_clientes.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_cliente(cliente_id: int, bd: Session = Depends(obtener_bd)):
    cliente = bd.query(ClienteBD).filter(ClienteBD.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id}, no existe",
        )
    return cliente


@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, bd: Session = Depends(obtener_bd)):
    cliente_bd = ClienteBD(**datos_cliente.model_dump())
    bd.add(cliente_bd)
    bd.commit()
    bd.refresh(cliente_bd)
    return cliente_bd


@rutas_clientes.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(
    cliente_id: int, datos_cliente: ClienteEditar, bd: Session = Depends(obtener_bd)
):
    cliente_bd = bd.query(ClienteBD).filter(ClienteBD.id == cliente_id).first()
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente con id {cliente_id} no existe.",
        )
    for campo, valor in datos_cliente.model_dump().items():
        setattr(cliente_bd, campo, valor)
    bd.commit()
    bd.refresh(cliente_bd)
    return cliente_bd


@rutas_clientes.delete("/clientes/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int, bd: Session = Depends(obtener_bd)):
    cliente_bd = bd.query(ClienteBD).filter(ClienteBD.id == cliente_id).first()
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente con id {cliente_id} no existe.",
        )
    bd.delete(cliente_bd)
    bd.commit()
    return cliente_bd
