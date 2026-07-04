from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .clientes import Cliente, ClienteRespuesta
from .transacciones import Transaccion, TransaccionRespuesta


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int | None = Field(default=None, foreign_key="cliente.id")

    cliente: Cliente = Relationship(back_populates="facturas")
    transacciones: list[Transaccion] = Relationship(back_populates="factura")


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(SQLModel):
    fecha: datetime


# Respuesta de la API: incluye cliente, transacciones y el total calculado
class FacturaRespuesta(FacturaBase):
    id: int
    cliente: ClienteRespuesta
    transacciones: list[TransaccionRespuesta] = []
    valor_total: float = 0.0
