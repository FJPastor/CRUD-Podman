from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.empleado_model import Empleado


class EmpleadoRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        #En el list se suelen incluir los campos más importantes, por lo que meto los relacionados por FK
        codDepartamento: Optional[int]=None, #posible solucion error dispositivo_service
        codEstado: Optional[int]=None,
        limit: Optional[int]=100,
        start: Optional[int]=0,
    ) -> List[Empleado]:
        query = self.db.query(Empleado)

        if nombre:
            #pruebo a meter un filtro de nombre que no sea estricto, no case ssensitive y no necesita nombre completo 
            query = query.filter(Empleado.nombre.ilike(f"%{nombre}%"))

        #return query.offset(start).limit(limit).all()
        print(f"Start*******************: {start}, Limit: {limit}, ")  # Depuración
        result = query.offset(start).limit(limit).all()
        print(f"Found ************{len(result)} records")  # Depuración
        #return query.offset(start).limit(limit).all()
        return result

    def get(self, empleado_id: int) -> Optional[Empleado]:
        return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
            Empleado,
            empleado_id,
           
        )

    
    def create(self, empleado: Empleado) -> Empleado:
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def update(self, id: int, empleado: Empleado) -> Empleado:
        # dispositivo.id = id #verificar si sobra esta linea
        #Sobra, porque dispositivo siempre va a tener el id que se le pasa en el body
        self.db.merge(empleado)
        self.db.commit()
        return empleado

    def delete(self, empleado: Empleado) -> None:
        try:
            self.db.delete(empleado)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting Empleado")

