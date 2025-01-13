from sqlalchemy import (
    Column,
    SmallInteger,
    PrimaryKeyConstraint,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from models.base_model import EntityMeta



class DepartamentoIdioma(EntityMeta):
    __tablename__ = "Departamento_Idioma"

    id = Column(SmallInteger, primary_key=True)
    codDepartamento = Column(SmallInteger, ForeignKey("Departamento.id"), nullable=False)
    codIdioma = Column(SmallInteger, nullable=False)
    nombre = Column(String(255), nullable=False)
   
    departamento = relationship(
        "Departamento",
        back_populates="idiomas", #relacion bidireccional
        lazy="select"
        
    )

    #PrimaryKeyConstraint(id)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "codDepartamento": self.codDepartamento.__str__(),
            "codIdioma": self.codIdioma.__str__(),
            "nombre": self.nombre.__str__(),
            
        }

from models.departamento_model import Departamento