from pydantic import BaseModel, computed_field
from datetime import datetime
from .clientes import Cliente
from .transacciones import Transaccion


# Modelo de facturas
class FacturaBase(BaseModel):
    fecha: str = datetime.now().strftime("%Y-%m-%d")
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        # Calcula el total sumando (cantidad * valor_unitario) de cada transaccion
        total_factura = 0.0
        if not self.transacciones:
            return total_factura
        for transaccion in self.transacciones:
            total_factura += transaccion.valor_unitario * transaccion.cantidad
        return total_factura


class FacturaCrear(BaseModel):
    fecha: str = datetime.now().strftime("%Y-%m-%d")


class FacturaEditar(BaseModel):
    fecha: str


class Factura(FacturaBase):
    id: int | None = None
