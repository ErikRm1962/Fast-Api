from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .facturas import Factura


# Campos que comparten todas las variantes de Cliente
class ClienteBase(SQLModel):
    nombre: str
    email: str
    descripcion: str | None = None


# Esta es la tabla real en la base de datos (table=True)
class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    facturas: list["Factura"] = Relationship(back_populates="cliente")


# Lo que se recibe al crear un cliente (sin id, lo genera la BD)
class ClienteCrear(ClienteBase):
    pass


# Lo que se recibe al editar un cliente
class ClienteEditar(ClienteBase):
    pass


# Lo que se devuelve en las respuestas de la API (con id)
class ClienteRespuesta(ClienteBase):
    id: int
