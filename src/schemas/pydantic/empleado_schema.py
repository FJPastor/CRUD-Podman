from typing import Optional
from pydantic import BaseModel
from datetime import date

#Esta clase se utiliza para validar los datos cuando se crea un nuevo tipo de dispositivo en un idioma específico.

class EmpleadoPostRequestSchema(BaseModel):
    id: int #no es autoincremental asi q lo incluimos
    codInstalacion: int
    codDepartamento: int
    nombre: str
    descripcion: str
    codigoEmpleado: str
    fechaAlta: date
    fechaBaja: Optional[date] #Añado optional porque en la tabla no hay fecha baja
    ubicacion: str
    codEstado: int

    


class EmpleadoSchema(EmpleadoPostRequestSchema):
    pass #Como el id no es autoincremental y lo incluimos arriba, aqui no hace falta volver a pasarlo, ya que lo hereda de la funcion superior
