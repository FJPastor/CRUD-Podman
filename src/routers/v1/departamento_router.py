from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.departamento_schema import (
    DepartamentoPostRequestSchema,
    DepartamentoSchema,
)

from services.departamento_service import DepartamentoService

DepartamentoRouter = APIRouter(prefix="/v1/Departamento", tags=["Departamento"])


@DepartamentoRouter.get("/", response_model=List[DepartamentoSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    departamentoService: DepartamentoService = Depends(),
  
):
    return [estado.normalize() for estado in departamentoService.list(nombre, pageSize, startIndex)]


@DepartamentoRouter.get("/{id}", response_model=DepartamentoSchema)
def get(id: int, departamentoService: DepartamentoService = Depends()):
    departamento = departamentoService.get(id)
    if departamento is None:
        raise HTTPException(status_code=404, detail="Estado not found")
    return departamento.normalize()

@DepartamentoRouter.post("/", response_model=DepartamentoSchema, status_code=status.HTTP_201_CREATED)
def create(departamento: DepartamentoSchema, departamentoService: DepartamentoService = Depends()):
    new_departamento = departamentoService.create(departamento)
    return new_departamento.normalize()


@DepartamentoRouter.put("/{id}", response_model=DepartamentoSchema)
def update(id: int, departamento: DepartamentoSchema, departamentoService: DepartamentoService = Depends()):
    existing_departamento = departamentoService.get(id)
    if existing_departamento is None:
        raise HTTPException(status_code=404, detail="Departamento not found")
    updated_departamento = departamentoService.update(id, departamento)
    return updated_departamento.normalize()



@DepartamentoRouter.delete("/{id}", status_code=204)
def delete(id: int, departamentoService: DepartamentoService = Depends()):
    departamentoService.delete(id)