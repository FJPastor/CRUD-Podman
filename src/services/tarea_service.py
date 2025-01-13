from typing import List, Optional

from fastapi import Depends, HTTPException
from models.tarea_model import Tarea

from repositories.tarea_repository import TareaRepository
from schemas.pydantic.tarea_schema import TareaSchema


class TareaService:
    tareaRepository: TareaRepository

    def __init__(self, tareaRepository: TareaRepository = Depends()) -> None:
        self.tareaRepository = tareaRepository

    def create(self, tarea_body: TareaSchema) -> Tarea:
        nuevo_tarea= Tarea(
            id=tarea_body.id,
            codEmpleado=tarea_body.codEmpleado,
            nombre=tarea_body.nombre,
            descripcion=tarea_body.descripcion,
            detalles=tarea_body.detalles,
            prioridad=tarea_body.prioridad,
            duracionEstimada=tarea_body.duracionEstimada,
            recursos=tarea_body.recursos,
            responsable=tarea_body.responsable,
            estado=tarea_body.estado,
            comentario=tarea_body.comentario,
        )
        return self.tareaRepository.create(nuevo_tarea)

    def delete(self, tarea_id: int) -> None:
        tarea= self.tareaRepository.get(tarea_id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea not found")
        self.tareaRepository.delete(tarea)

    def get(self, tarea_id: int) -> Tarea:
        return self.tareaRepository.get(tarea_id)

    def list(
        self,
        nombre: Optional[str] = None,
       # codDispositivo: Optional[int]=None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Tarea]:
       return self.tareaRepository.list(nombre=nombre,limit=pageSize,start=startIndex)

    def update(self, tarea_id: int, tarea_body: TareaSchema) -> Tarea:
        return self.tareaRepository.update(
            tarea_id, 
            Tarea(
                id=tarea_body.id,
                codEmpleado=tarea_body.codEmpleado,
                nombre=tarea_body.nombre,
                descripcion=tarea_body.descripcion,
                detalles=tarea_body.detalles,
                prioridad=tarea_body.prioridad,
                duracionEstimada=tarea_body.duracionEstimada,
                recursos=tarea_body.recursos,
                responsable=tarea_body.responsable,
                estado=tarea_body.estado,
                comentario=tarea_body.comentario,))

  
