from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    Date,
    Boolean,
    JSON
)
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta



class ReglaAsignacion(EntityMeta):
    __tablename__ = "ReglaAsignacion"

    id = Column(SmallInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    origen = Column(Integer, nullable=True)
    destino = Column(Integer, nullable=True)
    codTareaOrigen = Column(SmallInteger, ForeignKey("Tarea.id"), nullable=False)
    codTareaDestino = Column(SmallInteger, ForeignKey("Tarea.id"), nullable=False)

    tarea_origen = relationship(
        "Tarea",
        foreign_keys=[codTareaOrigen],
        back_populates="reglas_origen"
    )

    tarea_destino = relationship(
        "Tarea",
        foreign_keys=[codTareaDestino],
        back_populates="reglas_destino"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "nombre": self.nombre.__str__(),
            "descripcion": self.descripcion.__str__(),
            "origen": self.origen.__str__(),
            "destino": self.destino.__str__(),
            "codTareaOrigen": self.codTareaOrigen.__str__(),
            "codTareaDestino": self.codTareaDestino.__str__(),
        }
