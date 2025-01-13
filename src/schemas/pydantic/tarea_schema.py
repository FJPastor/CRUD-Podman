from typing import List
from pydantic import BaseModel
from datetime import date

#Esta clase se utiliza para validar los datos cuando se crea un nuevo tipo de dispositivo en un idioma específico.

class TareaPostRequestSchema(BaseModel):
    id: int #no es autoincremental asi q lo incluimos
    codEmpleado: int
    nombre: str
    descripcion: str
    detalles: List[str]
    prioridad: str
    duracionEstimada:str
    recursos: List[str]
    responsable:str
    estado: bool
    comentario: str



class TareaSchema(TareaPostRequestSchema):
    pass #Como el id no es autoincremental y lo incluimos arriba, aqui no hace falta volver a pasarlo, ya que lo hereda de la funcion superior
