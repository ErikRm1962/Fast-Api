from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..conexion_bd import obtener_bd
from ..modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteRespuesta

rutas_clientes = APIRouter()


# ENDPOINTS DE CLIENTES

@rutas_clientes.get("/clientes", response_model=list[ClienteRespuesta])
def listar_clientes(bd: Session = Depends(obtener_bd)):
    return bd.exec(select(Cliente)).all()


@rutas_clientes.get("/clientes/{cliente_id}", response_model=ClienteRespuesta)
def listar_cliente(cliente_id: int, bd: Session = Depends(obtener_bd)):
    cliente = bd.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id}, no existe",
        )
    return cliente


@rutas_clientes.post("/clientes", response_model=ClienteRespuesta)
def crear_cliente(datos_cliente: ClienteCrear, bd: Session = Depends(obtener_bd)):
    cliente = Cliente.model_validate(datos_cliente)
    bd.add(cliente)
    bd.commit()
    bd.refresh(cliente)
    return cliente


@rutas_clientes.patch("/clientes/{cliente_id}", response_model=ClienteRespuesta)
def editar_cliente(
    cliente_id: int, datos_cliente: ClienteEditar, bd: Session = Depends(obtener_bd)
):
    cliente = bd.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente con id {cliente_id} no existe.",
        )
    datos_actualizados = datos_cliente.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(cliente, campo, valor)
    bd.add(cliente)
    bd.commit()
    bd.refresh(cliente)
    return cliente


@rutas_clientes.delete("/clientes/{cliente_id}", response_model=ClienteRespuesta)
def eliminar_cliente(cliente_id: int, bd: Session = Depends(obtener_bd)):
    cliente = bd.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente con id {cliente_id} no existe.",
        )
    bd.delete(cliente)
    bd.commit()
    return cliente
