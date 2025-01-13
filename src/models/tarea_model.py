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

from models.reglaAsignacion_model import ReglaAsignacion


class Tarea(EntityMeta):
    __tablename__ = "Tarea"

    id = Column(SmallInteger, primary_key=True)
    codEmpleado = Column(SmallInteger, ForeignKey("Empleado.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    detalles = Column(JSON, nullable=True)
    prioridad = Column(String(255), nullable=True)
    duracionEstimada = Column(String(40), nullable=True)
    recursos = Column(JSON, nullable=True)
    responsable = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=True)
    comentario = Column(String(255), nullable=True)

    empleado = relationship(
        "Empleado",
        back_populates="tareas",
        lazy="select"
    )

    reglas_origen = relationship(
        "ReglaAsignacion",
        foreign_keys=[ReglaAsignacion.codTareaOrigen],
        back_populates="tarea_origen"
    )

    reglas_destino = relationship(
        "ReglaAsignacion",
        foreign_keys=[ReglaAsignacion.codTareaDestino],
        back_populates="tarea_destino"
    )

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "codEmpleado": self.codEmpleado.__str__(),
            "nombre": self.nombre.__str__(),
            "descripcion": self.descripcion.__str__(),
            "detalles": self.detalles,
            "prioridad": self.prioridad.__str__(),
            "duracionEstimada": self.duracionEstimada.__str__(),
            "recursos": self.recursos,
            "responsable": self.responsable.__str__(),
            "estado": self.estado.__str__(),
            "comentario": self.comentario.__str__(),
        }


from models.reglaAsignacion_model import ReglaAsignacion
from models.empleado_model import Empleado