from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .facturas import Factura


class TransaccionBase(SQLModel):
    cantidad: int
    valor_unitario: float


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")

    factura: "Factura" = Relationship(back_populates="transacciones")


class TransaccionCrear(TransaccionBase):
    pass


class TransaccionEditar(TransaccionBase):
    pass


class TransaccionRespuesta(TransaccionBase):
    id: int
    factura_id: int
