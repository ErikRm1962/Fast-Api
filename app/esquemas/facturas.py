from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from .clientes import Cliente
from .transacciones import Transaccion


class FacturaCrear(BaseModel):
    fecha: str = datetime.now().strftime("%Y-%m-%d")


class FacturaEditar(BaseModel):
    fecha: str


class Factura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: str
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        return sum(t.valor_unitario * t.cantidad for t in self.transacciones)
