from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.pydantic.tarea_schema import (
    TareaPostRequestSchema,
    TareaSchema,
)

from services.tarea_service import TareaService

TareaRouter = APIRouter(prefix="/v1/Tarea", tags=["Tarea"])


@TareaRouter.get("/", response_model=List[TareaSchema])
def index(
   # id: Optional[int] = None,
    nombre: Optional[str] = "",
    #codDispositivo: Optional[int]=None,
    pageSize: Optional[int] = 100,
    startIndex: Optional[int] = 0,
    tareaService: TareaService = Depends(),
  
):
    return [tarea.normalize() for tarea in tareaService.list(nombre=nombre, pageSize=pageSize, startIndex=startIndex)]


@TareaRouter.get("/{id}", response_model=TareaSchema)
def get(id: int, tareaService: TareaService = Depends()):
    tarea = tareaService.get(id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    return tarea.normalize()


@TareaRouter.post("/", response_model=TareaSchema, status_code=status.HTTP_201_CREATED)
def create(tarea: TareaSchema, tareaService: TareaService = Depends()):
    new_tarea = tareaService.create(tarea)
    return new_tarea.normalize()


@TareaRouter.put("/{id}", response_model=TareaSchema)
def update(id: int, tarea: TareaSchema, tareaService: TareaService = Depends()):
    existing_tarea = tareaService.get(id)
    if existing_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    updated_tarea = tareaService.update(id, tarea)
    return updated_tarea.normalize()



@TareaRouter.delete("/{id}", status_code=204)
def delete(id: int, tareaService: TareaService = Depends()):
    tareaService.delete(id)