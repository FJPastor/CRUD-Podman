from typing import List, Optional

from fastapi import Depends, HTTPException
from models.departamentoIdioma_model import DepartamentoIdioma

from repositories.departamentoIdioma_repository import DepartamentoIdiomaRepository
from schemas.pydantic.departamentoIdioma_schema import DepartamentoIdiomaSchema


class DepartamentoIdiomaService:
    departamentoIdiomaRepository: DepartamentoIdiomaRepository

    def __init__(self, departamentoIdiomaRepository: DepartamentoIdiomaRepository = Depends()) -> None:
        self.departamentoIdiomaRepository = departamentoIdiomaRepository

    def create(self, departamentoIdioma_body: DepartamentoIdiomaSchema) -> DepartamentoIdioma:
        return self.departamentoIdiomaRepository.create(
            DepartamentoIdioma(
                id=departamentoIdioma_body.id,
                codDepartamento=departamentoIdioma_body.codDepartamento,
                codIdioma=departamentoIdioma_body.codIdioma,
                nombre=departamentoIdioma_body.nombre))

    def delete(self, departamentoIdioma_id: int) -> None:
        departamento_idioma = self.departamentoIdiomaRepository.get(departamentoIdioma_id)
        if not departamento_idioma:
            raise HTTPException(status_code=404, detail="DepartamentoIdioma not found")
        self.departamentoIdiomaRepository.delete(departamento_idioma)

    def get(self, departamentoIdioma_id: int) ->Optional[DepartamentoIdioma]:
        return self.departamentoIdiomaRepository.get(departamentoIdioma_id)

    def list(
        self,
        nombre: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[DepartamentoIdioma]:
        return self.departamentoIdiomaRepository.list(nombre, limit=pageSize, start=startIndex)

    def update(self, departamentoIdioma_id: int, departamentoIdioma_body: DepartamentoIdiomaSchema) -> DepartamentoIdioma:
        return self.departamentoIdiomaRepository.update(
            departamentoIdioma_id,
            DepartamentoIdioma(
                id=departamentoIdioma_body.id,
                codDepartamento=departamentoIdioma_body.codDepartamento,
                codIdioma=departamentoIdioma_body.codIdioma,
                nombre=departamentoIdioma_body.nombre))

