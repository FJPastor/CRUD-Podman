from pydantic import BaseModel

class DepartamentoIdiomaPostRequestSchema(BaseModel):
    id: int
    codDepartamento: int
    codIdioma: int
    nombre: str



class DepartamentoIdiomaSchema(DepartamentoIdiomaPostRequestSchema):
    pass