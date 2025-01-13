from typing import List, Optional

from fastapi import Depends, HTTPException
from models.reglaAsignacion_model import ReglaAsignacion

from repositories.reglaAsignacion_repository import ReglaAsignacionRepository
from schemas.pydantic.reglaAsignacion_schema import ReglaAsignacionSchema


class ReglaAsignacionService:
    reglaAsignacionRepository: ReglaAsignacionRepository

    def __init__(self, reglaAsignacionRepository: ReglaAsignacionRepository = Depends()) -> None:
        self.reglaAsignacionRepository = reglaAsignacionRepository

    def create(self, reglaAsignacion_body: ReglaAsignacionSchema) -> ReglaAsignacion:
        nuevo_reglaDNat= ReglaAsignacion(
            id=reglaAsignacion_body.id,
            nombre=reglaAsignacion_body.nombre,
            descripcion=reglaAsignacion_body.descripcion,
            origen=reglaAsignacion_body.origen,
            destino=reglaAsignacion_body.destino,
            codTareaOrigen=reglaAsignacion_body.codTareaOrigen,
            codTareaDestino=reglaAsignacion_body.codTareaDestino,
        )
        return self.reglaAsignacionRepository.create(nuevo_reglaDNat)

    def delete(self, reglaAsignacion_id: int) -> None:
        reglaAsignacion= self.reglaAsignacionRepository.get(reglaAsignacion_id)
        if not reglaAsignacion:
            raise HTTPException(status_code=404, detail="ReglaDNat not found")
        self.reglaAsignacionRepository.delete(reglaAsignacion)


    def get(self, reglaAsignacion_id: int) -> Optional[ReglaAsignacion]:
        return self.reglaAsignacionRepository.get(reglaAsignacion_id)

    def list(
        self,
        nombre: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[ReglaAsignacion]:
       return self.reglaAsignacionRepository.list(nombre=nombre,limit=pageSize,start=startIndex)

    def update(self, reglaAsignacion_id: int, reglaAsignacion_body: ReglaAsignacionSchema) -> ReglaAsignacion:
        return self.reglaAsignacionRepository.update(
            reglaAsignacion_id, 
            ReglaAsignacion(
                id=reglaAsignacion_body.id,
                nombre=reglaAsignacion_body.nombre,
                descripcion=reglaAsignacion_body.descripcion,
                origen=reglaAsignacion_body.origen,
                destino=reglaAsignacion_body.destino,
                codTareaOrigen=reglaAsignacion_body.codTareaOrigen,
                codTareaDestino=reglaAsignacion_body.codTareaDestino,
            ))

  
