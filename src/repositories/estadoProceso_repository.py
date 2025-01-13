from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, lazyload

from configs.database import (
    get_db_connection,
)
from models.estado_proceso_model import EstadoProceso


class EstadoProcesoRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        nombre: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[EstadoProceso]:
        query = self.db.query(EstadoProceso)

        if nombre:
          #  query = query.filter_by(tipo=tipo)
            query = query.filter(EstadoProceso.nombre.contains(nombre))

        return query.offset(start).limit(limit).all()

    # def get(self, tipoDispositivo: TipoDispositivo) -> TipoDispositivo:   ME DA FALLO
    #     return self.db.get( #self.db.query si queremos añadir consulta con un inner, por ej o con un filtro
    #         TipoDispositivo,
    #         tipoDispositivo.id,
           
    #     )

    def get(self, estadoProceso_id: int) -> Optional[EstadoProceso]:

       # a=self.db.query(TipoDispositivo(id == tipoDispositivo_id))
       # a=self.db.query(TipoDispositivo).filter(TipoDispositivo.tipo == "tipo_dispositivo_test")
     #  return self.db.query(TipoDispositivo).filter(TipoDispositivo.id == tipoDispositivo_id).first()
        return self.db.get( #AQUI BREAKPOINT
            EstadoProceso,
            estadoProceso_id,
           # options=[lazyload(TipoDispositivo)],
        )



    def create(self, estadoProceso: EstadoProceso) -> EstadoProceso:
        self.db.add(estadoProceso)
        self.db.commit()
        self.db.refresh(estadoProceso)
        return estadoProceso

    def update(self, id: int, estadoProceso: EstadoProceso) -> EstadoProceso:
        # tipoDispositivo.id = id 
        self.db.merge(estadoProceso)
        self.db.commit()
        return estadoProceso


    def delete(self, estadoProceso: EstadoProceso) -> None:
        try:
            self.db.delete(estadoProceso)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting EstadoProceso")

