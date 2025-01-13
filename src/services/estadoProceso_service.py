from typing import List, Optional

from fastapi import Depends, HTTPException
from models.estado_proceso_model import EstadoProceso

from repositories.estadoProceso_repository import EstadoProcesoRepository
from schemas.pydantic.estadoProceso_schema import EstadoProcesoSchema


class EstadoProcesoService:
    estadoProcesoRepository: EstadoProcesoRepository

    def __init__(self, estadoProcesoRepository: EstadoProcesoRepository = Depends()) -> None:
        self.estadoProcesoRepository = estadoProcesoRepository

    def create(self, estadoProceso_body: EstadoProcesoSchema) -> EstadoProceso:
        return self.estadoProcesoRepository.create(
            EstadoProceso(
                id=estadoProceso_body.id,
                nombre=estadoProceso_body.nombre))


    def delete(self, estadoProceso_id: int) -> None:
        estadoProceso = self.estadoProcesoRepository.get(estadoProceso_id)
        if not estadoProceso:
            raise HTTPException(status_code=404, detail="estadoProceso not found")
        self.estadoProcesoRepository.delete(estadoProceso)



    def get(self, estadoProceso_id: int) -> Optional[EstadoProceso]:
        return self.estadoProcesoRepository.get(estadoProceso_id) #AQUI OTRO BREAKPOINT

    def list(
        self,
        nombre: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[EstadoProceso]:
        return self.estadoProcesoRepository.list(nombre=nombre, limit=pageSize, start=startIndex)

    def update(self, estadoProceso_id: int, estadoProceso_body: EstadoProcesoSchema) -> EstadoProceso:
        return self.estadoProcesoRepository.update(
            estadoProceso_id, #Identifica el tipo de dispositivo a actualizar
            EstadoProceso( #Crea un nuevo objeto de tipo TipoDispositivo con los datos del body que se quieren actualizar
                id=estadoProceso_body.id,
                nombre=estadoProceso_body.nombre))

  
