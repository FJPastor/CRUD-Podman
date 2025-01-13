from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.tarea_model import Tarea


class TareaRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        #En el list se suelen incluir los campos más importantes, por lo que meto los relacionados por FK
        codEmpleado: Optional[int]=None,
        limit: Optional[int]=100,
        start: Optional[int]=0,
    ) -> List[Tarea]:
        query = self.db.query(Tarea)

        if nombre:
            #pruebo a meter un filtro de nombre que no sea estricto, no case ssensitive y no necesita nombre completo 
            query = query.filter(Tarea.nombre.ilike(f"%{nombre}%"))

        print(f"Start*******************: {start}, Limit: {limit}")  # Depuración
        resultado = query.offset(start).limit(limit).all()
        print(f"Encontrados ************{len(resultado)} resultados")  # Depuración
        #return query.offset(start).limit(limit).all()
        return resultado

    def get(self, tarea_id: int) -> Optional[Tarea]:
        return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
            Tarea,
            tarea_id,
           
        )

    def create(self, tarea: Tarea) -> Tarea:
        self.db.add(tarea)
        self.db.commit()
        self.db.refresh(tarea)
        return tarea

    def update(self, id: int, tarea: Tarea) -> Tarea:
        # interfazRed.id = id #verificar si sobra esta linea
        self.db.merge(tarea)
        self.db.commit()
        return tarea

    def delete(self, tarea: Tarea) -> None:
        try:
            self.db.delete(tarea)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting Interfaz de Red")
