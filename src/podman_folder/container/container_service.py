from podman import PodmanClient
from typing import Dict, Iterable, List, Optional, Any
from loguru import logger
from podman_folder.container.podman_container import PodmanContainerRepository
from podman.domain.containers import Container as PodmanContainer

from podman_folder.model import PodmanContainerStatus, PodmanFilter
from podman.errors import APIError



class PodmanContainerService:
    # Inicializa el servicio con un repositorio de contenedores
    #por lo que no tenemos que llamar al cliente Podman directamente cada vez que necesitemos interactuar con el contenedor
    def __init__(self, repository: PodmanContainerRepository):
        self.repository = repository


    def list_containers(self, status: PodmanContainerStatus) -> Iterable[PodmanContainer]:
        logger.info(f"CONTAINER | list | status[{status.value}]")
        filters = PodmanFilter()  # crea una instancia de PodmanFilter, para filtrar los contenedores por status
        if status != PodmanContainerStatus.all: # si el status no es all
            filters.status = status.name  # asigna el status al filtro
        all__ = True if status == PodmanContainerStatus.all else False  # si el status es all, all__ es True
        # Loguear los filtros antes de pasarlos al repositorio
        logger.info(f"Using filters: {filters.to_dict()}")
        #lista los contenedores con los filtros y el status
        containers = self.repository.list(all_=all__, filters=filters)  # llama al método list de PodmanContainerRepository
        return containers

    #El create no lo uso porque uso el run, que crea y corre el contenedor
    def create_container(self, image: str, name: str, command: Optional[List[Any]] = None) -> PodmanContainer:
        return self.repository.create(image=image, name=name, command=command)

    #El fetch_container lo usamos para obtener un contenedor por su id
    def fetch_container(self, id_: str) -> Optional[PodmanContainer]:
        logger.info(f"CONTAINER | fetch | id[{id_}]")
        # filters = PodmanFilter()

        try:
            container = self.repository.fetch(id_) #llama al método fetch del repositorio
            logger.info(f"Fetched container: {container.attrs}")  # depurar los atributos del contenedor

            return container
        except APIError as e:
            logger.warning(f"CONTAINER | fetch | error >> {e}")
            raise
 
#El run_container lo usamos para crear y correr un contenedor
    def run_container(self, image: str, name: str, environment=None, labels=None, command: Optional[List[Any]] = None) -> PodmanContainer:
        return self.repository.run(image=image, name=name, environment=environment, labels=labels, command=command)

    def copy_into_container(self, container: PodmanContainer, source: str, destination: str):
        self.repository.copy_into_container(container, source, destination)

    def start_container(self, container: PodmanContainer) -> Any:
        return self.repository.start(container)

    def stop_container(self, container: PodmanContainer) -> Any:
        return self.repository.stop(container)

    def kill_container(self, container: PodmanContainer) -> Any:
        return self.repository.kill(container)

    def restart_container(self, container: PodmanContainer) -> Any:
        return self.repository.restart(container)

    def remove_container(self, container: PodmanContainer) -> Any:
        return self.repository.remove(container)
    
    #El run_container_with_secrets lo usamos para correr un contenedor con secretos
    def run_container_with_secrets(self, image: str, name: str, environment=None, labels=None, command: Optional[List[Any]] = None, secrets: Optional[List[str]]= None) -> PodmanContainer:
        return self.repository.run_container_secrets(image=image,name=name,environment=environment,labels=labels,command=command,secrets=secrets)  # Pasamos los secretos
        

# Al hacer el run, si queremos que se mantengna en uso de forma indefinida, tenemos que añadir en commands: ["tail", "-f", "/dev/null"]
# {
#   "environment": {
#     "additionalProp1": "string",
#     "additionalProp2": "string",
#     "additionalProp3": "string"
#   },
#   "labels": {
#     "additionalProp1": "string",
#     "additionalProp2": "string",
#     "additionalProp3": "string"
#   },
#   "command": [
#     "tail",
#     "-f",
#     "/dev/null"
#   ],
#   "secrets": [
#     "user"
#   ]
# }