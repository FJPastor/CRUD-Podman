from pydantic import BaseModel

#Esta clase se utiliza para validar los datos cuando se crea un nuevo tipo de dispositivo en un idioma específico.

class EstadoProcesoPostRequestSchema(BaseModel):
    id: int #no es autoincremental asi q lo incluimos
    nombre: str


class EstadoProcesoSchema(EstadoProcesoPostRequestSchema):
    pass #Como el id no es autoincremental y lo incluimos arriba, aqui no hace falta volver a pasarlo, ya que lo hereda de la funcion superior
