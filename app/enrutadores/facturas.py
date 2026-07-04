from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..conexion_bd import obtener_bd
from ..modelos.clientes import ClienteBD
from ..modelos.facturas import FacturaBD
from ..esquemas.facturas import Factura, FacturaCrear, FacturaEditar

rutas_facturas = APIRouter()


# ENDPOINTS DE FACTURAS

@rutas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(bd: Session = Depends(obtener_bd)):
    return bd.query(FacturaBD).all()


@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int, bd: Session = Depends(obtener_bd)):
    factura = bd.query(FacturaBD).filter(FacturaBD.id == factura_id).first()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    return factura


@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(
    cliente_id: int, datos_factura: FacturaCrear, bd: Session = Depends(obtener_bd)
):
    cliente = bd.query(ClienteBD).filter(ClienteBD.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id}, no existe.",
        )
    factura_bd = FacturaBD(fecha=datos_factura.fecha, cliente_id=cliente_id)
    bd.add(factura_bd)
    bd.commit()
    bd.refresh(factura_bd)
    return factura_bd


@rutas_facturas.patch("/facturas/{factura_id}", response_model=Factura)
async def editar_factura(
    factura_id: int, datos_factura: FacturaEditar, bd: Session = Depends(obtener_bd)
):
    factura_bd = bd.query(FacturaBD).filter(FacturaBD.id == factura_id).first()
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    factura_bd.fecha = datos_factura.fecha
    bd.commit()
    bd.refresh(factura_bd)
    return factura_bd


@rutas_facturas.delete("/facturas/{factura_id}", response_model=Factura)
async def eliminar_factura(factura_id: int, bd: Session = Depends(obtener_bd)):
    factura_bd = bd.query(FacturaBD).filter(FacturaBD.id == factura_id).first()
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    bd.delete(factura_bd)
    bd.commit()
    return factura_bd
