from pydantic import BaseModel


# Modelo de transacciones
class TransaccionBase(BaseModel):
    cantidad: int
    valor_unitario: float


class TransaccionCrear(TransaccionBase):
    pass


class TransaccionEditar(TransaccionBase):
    pass


class Transaccion(TransaccionBase):
    id: int | None = None
    factura_id: int | None = None  # relación con el modelo factura
