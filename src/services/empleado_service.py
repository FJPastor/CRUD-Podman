from typing import List, Optional

from fastapi import Depends, HTTPException
from models.empleado_model import Empleado

from repositories.empleado_repository import EmpleadoRepository
from schemas.pydantic.empleado_schema import EmpleadoSchema


class EmpleadoService:
    empleadoRepository: EmpleadoRepository

    def __init__(self, empleadoRepository: EmpleadoRepository = Depends()) -> None:
        self.empleadoRepository = empleadoRepository

    def create(self, empleado_body: EmpleadoSchema) -> Empleado:
        #Como tiene mas campos, pruebo a hacerlo de esta manera
        nuevo_empleado= Empleado(
            id=empleado_body.id,
            codInstalacion=empleado_body.codInstalacion,
            codDepartamento=empleado_body.codDepartamento,
            nombre=empleado_body.nombre,
            descripcion=empleado_body.descripcion,
            codigoEmpleado=empleado_body.codigoEmpleado,
            fechaAlta=empleado_body.fechaAlta,
            fechaBaja=empleado_body.fechaBaja,
            ubicacion=empleado_body.ubicacion,
            codEstado=empleado_body.codEstado,
        )
        return self.empleadoRepository.create(nuevo_empleado)

    def delete(self, empleado_id: int) -> None:
        empleado= self.empleadoRepository.get(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="empleado not found")
        self.empleadoRepository.delete(empleado)

    def get(self, empleado_id: int) -> Optional[Empleado]:
        return self.empleadoRepository.get(empleado_id)

    

    def list(
        self,
        nombre: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Empleado]:
       return self.empleadoRepository.list(nombre=nombre,limit=pageSize,start=startIndex)

    def update(self, empleado_id: int, empleado_body: EmpleadoSchema) -> Empleado:
        return self.empleadoRepository.update(
            empleado_id, 
            Empleado(
                id=empleado_body.id,
                codInstalacion=empleado_body.codInstalacion,
                codDepartamento=empleado_body.codDepartamento,
                nombre=empleado_body.nombre,
                descripcion=empleado_body.descripcion,
                codigoEmpleado=empleado_body.codigoEmpleado,
                fechaAlta=empleado_body.fechaAlta,
                fechaBaja=empleado_body.fechaBaja,
                ubicacion=empleado_body.ubicacion,
                codEstado=empleado_body.codEstado))

  
