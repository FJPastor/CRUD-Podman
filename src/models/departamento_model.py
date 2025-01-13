from sqlalchemy import (
    Column,
    SmallInteger,
    PrimaryKeyConstraint,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta



class Departamento(EntityMeta):
    __tablename__ = "Departamento"

    id = Column(SmallInteger,primary_key=True)
    nombre = Column(String(255), nullable=False)
    idiomas = relationship(
        "DepartamentoIdioma",
        back_populates="departamento", #relacion bidireccional
        lazy="select",
        
    )

    empleados = relationship(
        "Empleado",
        back_populates="departamento", #relacion bidireccional
        lazy="select",
    )

    #PrimaryKeyConstraint(id) no necesario, lo pongo al declarar las variables

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "nombre": self.nombre.__str__(),
            
        }

from models.departamentoIdioma_model import DepartamentoIdioma
from models.empleado_model import Empleado