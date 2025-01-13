from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.departamento_model import Departamento


class DepartamentoRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Departamento]:
        query = self.db.query(Departamento)

        if nombre:
            query = query.filter_by(nombre=nombre)

        return query.offset(start).limit(limit).all()

    def get(self, departamento_id: int) -> Optional[Departamento]:
        return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
            Departamento,
            departamento_id,
        )

    def create(self, departamento: Departamento) -> Departamento:
        self.db.add(departamento)
        self.db.commit()
        self.db.refresh(departamento)
        return departamento

    def update(self, id: int, departamento: Departamento) -> Departamento:
        # estado.id = id #verificar si sobra esta linea
        self.db.merge(departamento)
        self.db.commit()
        return departamento

    def delete(self, departamento: Departamento) -> None:
        try:
            self.db.delete(departamento)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting Departamento")
