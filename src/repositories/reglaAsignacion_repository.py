from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.reglaAsignacion_model import ReglaAsignacion


class ReglaAsignacionRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        #En el list se suelen incluir los campos más importantes, por lo que meto los relacionados por FK
        codTareaOrigen: Optional[int]=None, 
        codTareaDestino: Optional[int]=None,
        limit: Optional[int]=100,
        start: Optional[int]=0,
    ) -> List[ReglaAsignacion]:
        query = self.db.query(ReglaAsignacion)

        if nombre:
            #pruebo a meter un filtro de nombre que no sea estricto, no case ssensitive y no necesita nombre completo 
            query = query.filter(ReglaAsignacion.nombre.ilike(f"%{nombre}%"))

        return query.offset(start).limit(limit).all()

    def get(self, regla_id: int) -> Optional[ReglaAsignacion]:
        return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
            ReglaAsignacion,
            regla_id,
           
        )

    def create(self, regla: ReglaAsignacion) -> ReglaAsignacion:
        self.db.add(regla)
        self.db.commit()
        self.db.refresh(regla)
        return regla

    def update(self, id: int, regla: ReglaAsignacion) -> ReglaAsignacion:
        # reglaDNat.id = id #verificar si sobra esta linea
        self.db.merge(regla)
        self.db.commit()
        return regla

    def delete(self, regla: ReglaAsignacion) -> None:
        try:
            self.db.delete(regla)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting Regla de Asignacion")
