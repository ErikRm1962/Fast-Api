from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion_bd import Base


class FacturaBD(Base):
    __tablename__ = "factura"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("ClienteBD", back_populates="facturas")
    transacciones = relationship(
        "TransaccionBD", back_populates="factura", cascade="all, delete-orphan"
    )
