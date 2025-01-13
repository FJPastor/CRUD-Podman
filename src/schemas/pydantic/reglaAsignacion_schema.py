from pydantic import BaseModel, Field, constr

class ReglaAsignacionPostRequestSchema(BaseModel):
    id:int #no es autoincremental asi q lo incluimos
    nombre: str
    descripcion: str
    origen: int
    destino: int
    codTareaOrigen: int
    codTareaDestino: int
    

class ReglaAsignacionSchema(ReglaAsignacionPostRequestSchema):
    pass #Como el id no es autoincremental y lo incluimos arriba, aqui no hace falta volver a pasarlo, ya que lo hereda de la funcion superior