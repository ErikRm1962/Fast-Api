from pydantic import BaseModel, ConfigDict


class TransaccionBase(BaseModel):
    cantidad: int
    valor_unitario: float


class TransaccionCrear(TransaccionBase):
    pass


class TransaccionEditar(TransaccionBase):
    pass


class Transaccion(TransaccionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    factura_id: int
