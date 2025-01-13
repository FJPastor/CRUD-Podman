from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.estadoProceso_schema import (
    EstadoProcesoPostRequestSchema,
    EstadoProcesoSchema,
)

from services.estadoProceso_service import EstadoProcesoService

EstadoProcesoRouter = APIRouter(prefix="/v1/EstadoProceso", tags=["EstadoProceso"])


@EstadoProcesoRouter.get("/", response_model=List[EstadoProcesoSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    estadoProcesoService: EstadoProcesoService = Depends(),
  
):
    return [estadoProceso.normalize() for estadoProceso in estadoProcesoService.list(nombre, pageSize, startIndex)]


@EstadoProcesoRouter.get("/{id}", response_model=EstadoProcesoSchema)
def get(id: int, estadoProcesoService: EstadoProcesoService = Depends()):
    estadoProceso = estadoProcesoService.get(id)
    if estadoProceso is None:
        raise HTTPException(status_code=404, detail="EstadoProceso not found")
    return estadoProceso.normalize()

@EstadoProcesoRouter.post("/", response_model=EstadoProcesoSchema, status_code=status.HTTP_201_CREATED)
def create(estadoProceso: EstadoProcesoSchema, estadoProcesoService: EstadoProcesoService = Depends()):
    new_estadoProceso = estadoProcesoService.create(estadoProceso)
    return new_estadoProceso.normalize()


@EstadoProcesoRouter.put("/{id}", response_model=EstadoProcesoSchema)
def update(id: int, estadoProceso: EstadoProcesoSchema, estadoProcesoService: EstadoProcesoService = Depends()):
    existing_estadoProceso = estadoProcesoService.get(id)
    if existing_estadoProceso is None:
        raise HTTPException(status_code=404, detail="estadoProceso not found")
    updated_estadoProceso = estadoProcesoService.update(id, estadoProceso)
    return updated_estadoProceso.normalize()



@EstadoProcesoRouter.delete("/{id}", status_code=204)
def delete(id: int, estadoProcesoService: EstadoProcesoService = Depends()):
    estadoProcesoService.delete(id)
