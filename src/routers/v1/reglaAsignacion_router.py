from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.reglaAsignacion_schema import (
    ReglaAsignacionPostRequestSchema,
    ReglaAsignacionSchema,
)

from services.reglaAsignacion_service import ReglaAsignacionService

ReglaAsignacionRouter = APIRouter(prefix="/v1/ReglaAsignacion", tags=["ReglaAsignacion"])


@ReglaAsignacionRouter.get("/", response_model=List[ReglaAsignacionSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    reglaAsignacionService: ReglaAsignacionService = Depends(),
  
):
    return [reglaAsignacion.normalize() for reglaAsignacion in reglaAsignacionService.list(nombre, pageSize, startIndex)]


@ReglaAsignacionRouter.get("/{id}", response_model=ReglaAsignacionSchema)
def get(id: int, reglaAsignacionService: ReglaAsignacionService = Depends()):
    reglaAsignacion = reglaAsignacionService.get(id)
    if reglaAsignacion is None:
        raise HTTPException(status_code=404, detail="Regla Asignacion not found")
    return reglaAsignacion.normalize()


@ReglaAsignacionRouter.post("/", response_model=ReglaAsignacionSchema, status_code=status.HTTP_201_CREATED)
def create(reglaAsignacion: ReglaAsignacionSchema, reglaAsignacionService: ReglaAsignacionService = Depends()):
    new_reglaAsignacion = reglaAsignacionService.create(reglaAsignacion)
    return new_reglaAsignacion.normalize()


@ReglaAsignacionRouter.put("/{id}", response_model=ReglaAsignacionSchema)
def update(id: int, reglaAsignacion: ReglaAsignacionSchema, reglaAsignacionService: ReglaAsignacionService = Depends()):
    existing_reglaAsignacion = reglaAsignacionService.get(id)
    if existing_reglaAsignacion is None:
        raise HTTPException(status_code=404, detail="ReglaAsignacion not found")
    updated_reglaAsignacion = reglaAsignacionService.update(id, reglaAsignacion)
    return updated_reglaAsignacion.normalize()



@ReglaAsignacionRouter.delete("/{id}", status_code=204)
def delete(id: int, reglaAsignacionService: ReglaAsignacionService = Depends()):
    reglaAsignacionService.delete(id)