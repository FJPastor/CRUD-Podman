from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.departamentoIdioma_schema import (
    DepartamentoIdiomaPostRequestSchema,
    DepartamentoIdiomaSchema,
)

from services.departamentoIdioma_service import DepartamentoIdiomaService

DepartamentoIdiomaRouter = APIRouter(prefix="/v1/DepartamentoIdioma", tags=["Departamento_Idioma"])


@DepartamentoIdiomaRouter.get("/", response_model=List[DepartamentoIdiomaSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    departamentoIdiomaService: DepartamentoIdiomaService = Depends(),
  
):
    return [departamentoIdioma.normalize() for departamentoIdioma in departamentoIdiomaService.list(nombre, pageSize, startIndex)]


@DepartamentoIdiomaRouter.get("/{id}", response_model=DepartamentoIdiomaSchema)
def get(id: int, departamentoIdiomaService: DepartamentoIdiomaService = Depends()):
    departamentoIdioma = departamentoIdiomaService.get(id)
    if departamentoIdioma is None:
        raise HTTPException(status_code=404, detail="departamentoIdioma not found")
    return departamentoIdioma.normalize()

@DepartamentoIdiomaRouter.post("/", response_model=DepartamentoIdiomaSchema, status_code=status.HTTP_201_CREATED)
def create(departamentoIdioma: DepartamentoIdiomaSchema, departamentoIdiomaService: DepartamentoIdiomaService = Depends()):
    new_departamentoIdioma = departamentoIdiomaService.create(departamentoIdioma)
    return new_departamentoIdioma.normalize()

@DepartamentoIdiomaRouter.put("/{id}", response_model=DepartamentoIdiomaSchema)
def update(id: int,departamentoIdioma: DepartamentoIdiomaSchema, departamentoService: DepartamentoIdiomaService = Depends()):
    existing_departamentoIdioma = departamentoService.get(id)
    if existing_departamentoIdioma is None:
        raise HTTPException(status_code=404, detail="departamentoIdioma not found")
    updated_departamentoIdioma = departamentoService.update(id, departamentoIdioma)
    return updated_departamentoIdioma.normalize()

@DepartamentoIdiomaRouter.delete("/{id}", status_code=204)
def delete(id: int, departamentoIdiomaService: DepartamentoIdiomaService = Depends()):
    departamentoIdiomaService.delete(id)