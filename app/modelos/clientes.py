from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..conexion_bd import Base


class ClienteBD(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    facturas = relationship(
        "FacturaBD", back_populates="cliente", cascade="all, delete-orphan"
    )
