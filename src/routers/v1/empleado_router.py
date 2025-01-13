from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.empleado_schema import (
    EmpleadoPostRequestSchema,
    EmpleadoSchema,
)

from services.empleado_service import EmpleadoService

EmpleadoRouter = APIRouter(prefix="/v1/Empleado", tags=["Empleado"])


@EmpleadoRouter.get("/", response_model=List[EmpleadoSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    empleadoService: EmpleadoService = Depends(),
  
):
    return [empleado.normalize() for empleado in empleadoService.list(nombre, pageSize, startIndex)]


@EmpleadoRouter.get("/{id}", response_model=EmpleadoSchema)
def get(id: int, empleadoService: EmpleadoService = Depends()):
    empleado = empleadoService.get(id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado not found")
    return empleado.normalize()

@EmpleadoRouter.post("/", response_model=EmpleadoSchema, status_code=status.HTTP_201_CREATED)
def create(empleado: EmpleadoSchema, empleadoService: EmpleadoService = Depends()):
    new_empleado = empleadoService.create(empleado)
    return new_empleado.normalize()


@EmpleadoRouter.put("/{id}", response_model=EmpleadoSchema)
def update(id: int, empleado: EmpleadoSchema, empleadoService: EmpleadoService = Depends()):
    existing_empleado = empleadoService.get(id)
    if existing_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado not found")
    updated_empleado = empleadoService.update(id, empleado)
    return updated_empleado.normalize()



@EmpleadoRouter.delete("/{id}", status_code=204)
def delete(id: int, empleadoService: EmpleadoService = Depends()):
    empleadoService.delete(id)