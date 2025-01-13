from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.departamentoIdioma_model import DepartamentoIdioma


class DepartamentoIdiomaRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[DepartamentoIdioma]:
        query = self.db.query(DepartamentoIdioma)

        if nombre:
            query = query.filter_by(nombre=nombre)

        return query.offset(start).limit(limit).all()

    def get(self, departamentoIdioma_id: int) -> Optional[DepartamentoIdioma]:
        return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
            DepartamentoIdioma,
            departamentoIdioma_id,
        )

    def create(self, departamentoIdioma: DepartamentoIdioma) -> DepartamentoIdioma:
        self.db.add(departamentoIdioma)
        self.db.commit()
        self.db.refresh(departamentoIdioma)
        return departamentoIdioma

    def update(self, id: int, departamentoIdioma: DepartamentoIdioma) -> DepartamentoIdioma:
        self.db.merge(departamentoIdioma)
        self.db.commit()
        return departamentoIdioma

    def delete(self, departamentoIdioma: DepartamentoIdioma) -> None:
        try:
            self.db.delete(departamentoIdioma)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting DepartamentoIdioma")

