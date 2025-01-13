from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    Date
)
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta



class Empleado(EntityMeta):
    __tablename__ = "Empleado"

    id = Column(SmallInteger, primary_key=True)
    codInstalacion = Column(SmallInteger, nullable=True)
    codDepartamento = Column(SmallInteger, ForeignKey("Departamento.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    codigoEmpleado = Column(String(255), nullable=True)
    fechaAlta = Column(Date, nullable=True)
    fechaBaja = Column(Date, nullable=True)
    ubicacion = Column(String(255), nullable=True)
    codEstado = Column(SmallInteger, ForeignKey("EstadoProceso.id"), nullable=False)


    departamento = relationship(
        "Departamento",
        back_populates="empleados",
        lazy="select"
    )

    estado = relationship(
        "EstadoProceso",
        back_populates="empleados",
        lazy="select"
    )

    tareas = relationship(
        "Tarea",
        back_populates="empleado",
        lazy="select"
    )
    #PrimaryKeyConstraint(id) no necesario, lo pongo al declarar las variables

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "codInstalacion": self.codInstalacion.__str__(),
            "codDepartamento": self.codDepartamento.__str__(),
            "nombre": self.nombre.__str__(),
            "descripcion": self.descripcion.__str__(),
            "codigoEmpleado": self.codigoEmpleado.__str__(),
            "fechaAlta": self.fechaAlta.__str__() if self.fechaAlta is not None else None,
            "fechaBaja": self.fechaBaja.__str__() if self.fechaBaja is not None else None,
            "ubicacion": self.ubicacion.__str__(),
            "codEstado": self.codEstado.__str__(),
        }

from models.estado_proceso_model import EstadoProceso
from models.departamento_model import Departamento
from models.tarea_model import Tarea