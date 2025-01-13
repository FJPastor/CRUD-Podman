from sqlalchemy import (
    Column,
    SmallInteger,
    PrimaryKeyConstraint,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta



class EstadoProceso(EntityMeta):
    __tablename__ = "EstadoProceso"

    id = Column(SmallInteger,primary_key=True)
    nombre = Column(String(255), nullable=False)
    
    empleados = relationship(
        "Empleado",
     #   lazy="dynamic",
        back_populates="estado" #relacion bidireccional con la tabla estado
    )


    #PrimaryKeyConstraint(id) no necesario, lo pongo al declarar las variables

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "nombre": self.nombre.__str__(),
            
        }


from models.empleado_model import Empleado