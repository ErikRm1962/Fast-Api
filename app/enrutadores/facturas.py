from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..conexion_bd import obtener_bd
from ..modelos.clientes import Cliente
from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar, FacturaRespuesta

rutas_facturas = APIRouter()


def calcular_respuesta_factura(factura: Factura) -> FacturaRespuesta:
    """Arma la respuesta de la factura incluyendo el valor_total calculado."""
    valor_total = sum(t.valor_unitario * t.cantidad for t in factura.transacciones)
    return FacturaRespuesta(
        id=factura.id,
        fecha=factura.fecha,
        cliente=factura.cliente,
        transacciones=factura.transacciones,
        valor_total=valor_total,
    )


# ENDPOINTS DE FACTURAS

@rutas_facturas.get("/facturas", response_model=list[FacturaRespuesta])
def listar_facturas(bd: Session = Depends(obtener_bd)):
    facturas = bd.exec(select(Factura)).all()
    return [calcular_respuesta_factura(f) for f in facturas]


@rutas_facturas.get("/facturas/{factura_id}", response_model=FacturaRespuesta)
def listar_factura(factura_id: int, bd: Session = Depends(obtener_bd)):
    factura = bd.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    return calcular_respuesta_factura(factura)


@rutas_facturas.post("/facturas/{cliente_id}", response_model=FacturaRespuesta)
def crear_factura(
    cliente_id: int, datos_factura: FacturaCrear, bd: Session = Depends(obtener_bd)
):
    cliente = bd.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id}, no existe.",
        )
    factura = Factura(fecha=datos_factura.fecha, cliente_id=cliente_id)
    bd.add(factura)
    bd.commit()
    bd.refresh(factura)
    return calcular_respuesta_factura(factura)


@rutas_facturas.patch("/facturas/{factura_id}", response_model=FacturaRespuesta)
def editar_factura(
    factura_id: int, datos_factura: FacturaEditar, bd: Session = Depends(obtener_bd)
):
    factura = bd.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    factura.fecha = datos_factura.fecha
    bd.add(factura)
    bd.commit()
    bd.refresh(factura)
    return calcular_respuesta_factura(factura)


@rutas_facturas.delete("/facturas/{factura_id}", response_model=FacturaRespuesta)
def eliminar_factura(factura_id: int, bd: Session = Depends(obtener_bd)):
    factura = bd.get(Factura, factura_id)
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe",
        )
    respuesta = calcular_respuesta_factura(factura)
    bd.delete(factura)
    bd.commit()
    return respuesta
