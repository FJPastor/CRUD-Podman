from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException

class PodmanContainerSchema(BaseModel):
    id: Optional[str]
    image: Optional[str]
    name: Optional[str]
    status: Optional[str]
    labels: Optional[Dict[str, Any]]

    class Config:
        arbitrary_types_allowed = True

    #hacemos un metodo exclusivo para el list, ya que me generaba conflicto
    #el de abajo funciona al obtener un solo contenedor de la lista, pero para obtener la lista de contenedores
    #no funcionaba, porque el name en este metodo tiene que ser una lista y en el from es solo un string
    @classmethod
    def from_container_list(cls, container):
        return cls(
            id=container.attrs['Id'],
            image=str(container.attrs['Image']),
            name=container.attrs['Names'][0] if container.attrs['Names'] else None,
            status=container.attrs['State'],
            labels=container.attrs.get('Labels', {})
        )

    @classmethod
    def from_container(cls, container):
        # Verifica el contenido de container.attrs para depuración
        print("Container attributes:", container.attrs)

        # Acceso al nombre del contenedor
        name = container.attrs.get('Name', None)  # Obtener 'Name' o None si no existe

        return cls(
            id=container.attrs['Id'],
            image=str(container.attrs['Image']),
            name=name,  # Asigna el nombre directamente
            status=container.attrs['State']['Status'],  # Asegúrate de que 'State' tiene 'Status'
            labels=container.attrs.get('Labels', {})
        )