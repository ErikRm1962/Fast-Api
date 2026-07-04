from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..conexion_bd import Base


class TransaccionBD(Base):
    __tablename__ = "transaccion"

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    factura_id = Column(Integer, ForeignKey("factura.id"), nullable=False)

    factura = relationship("FacturaBD", back_populates="transacciones")
