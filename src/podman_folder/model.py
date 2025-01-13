from enum import Enum
from typing import Iterable, List, Optional, Union
from pydantic import BaseModel

#tenia la variable en mayusculas y no funcionaba, lo paso a minusculas y funciona bien
class PodmanContainerStatus(Enum):
    unknown = "unknown"
    running = "running"
    paused = "paused"
    stopped = "stopped"
    exited = "exited"
    restarting = "restarting"
    created = "created"
    all= "all"

#filtro que usamos en el list de contenedores
class PodmanFilter(BaseModel):
    exited: Optional[int] = None
    status: Optional[str]= None
    label: Optional[Union[str,List[str]]]= None
    id: Optional[str]= None
    name: Optional[str]= None
    ancestor: Optional[str]= None
    before: Optional[str]= None
    since: Optional[str]= None

    



    class config:
        use_enum_values = True #Convierte Eum en string

    def to_dict(self):
        return self.dict(exclude_none=True)

#modelo de contenedor, aunque realmente usamos el de la propia libreria de podman
class PodmanContainer(BaseModel):
    id: str
    name: str
    image: str
    status: PodmanContainerStatus
    created: str
    ports: Optional[Iterable[str]] = None
    labels: Optional[dict] = None

#modelo de imagen, aunque realmente usamos el de la propia libreria de podman
class PodmanImage(BaseModel):
    id: str
    name: str
    tag: Optional[str] = None
    size: Optional[int] = None