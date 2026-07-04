from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    nombre: str
    email: str
    descripcion: str | None = None


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
