from typing import List, Optional

from fastapi import Depends, HTTPException
from models.departamento_model import Departamento

from repositories.departamento_repository import DepartamentoRepository
from schemas.pydantic.departamento_schema import DepartamentoSchema


class DepartamentoService:
    departamentoRepository: DepartamentoRepository

    def __init__(self, departamentoRepository: DepartamentoRepository = Depends()) -> None:
        self.departamentoRepository = departamentoRepository

    def create(self, departamento_body: DepartamentoSchema) -> Departamento:
        nuevo_departamento = Departamento(
            id=departamento_body.id,
            nombre=departamento_body.nombre,
        )
        return self.departamentoRepository.create(nuevo_departamento)

    def delete(self, departamento_id: int) -> None:
        departamento = self.departamentoRepository.get(departamento_id)
        if not departamento:
            raise HTTPException(status_code=404, detail="Departamento not found")
        self.departamentoRepository.delete(departamento)


    def get(self, departamento_id: int) -> Optional[Departamento]:
        return self.departamentoRepository.get(departamento_id)

    def list(
        self,
        nombre: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Departamento]:
        return self.departamentoRepository.list(nombre=nombre, limit=pageSize, start=startIndex)

    def update(self,departamento_id: int, departamento_body: DepartamentoSchema) -> Departamento:
        return self.departamentoRepository.update(
            departamento_id, 
            Departamento(id=departamento_body.id, 
                   nombre=departamento_body.nombre))

