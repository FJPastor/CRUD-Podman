from fastapi import FastAPI, Depends, HTTPException
from typing import List, Dict, Any, Optional
from podman import PodmanClient
from podman.domain.containers import Container as PodmanContainer
from pydantic import BaseModel
from podman_folder.container.container_schema import PodmanContainerSchema
from podman_folder.container.container_service import PodmanContainerService
from podman_folder.container.podman_container import PodmanContainerRepository
from fastapi import APIRouter

from podman_folder.model import PodmanContainerStatus


ContainerRouter = APIRouter(prefix="/v1/Container", tags=["Containers"])


def get_podman_client() -> PodmanClient:
    return PodmanClient(base_url="tcp://localhost:8082")


#RECORDAR EN LA TERMINAL: podman system service -t 0 tcp:localhost:8082


# def get_podman_service(client: PodmanClient) -> PodmanContainerService:
#     repository = PodmanContainerRepository(client)
#     return PodmanContainerService(repository)

def get_podman_service() -> PodmanContainerService:
    client = get_podman_client()
    repository = PodmanContainerRepository(client)
    return PodmanContainerService(repository)

#PODRIAMOS HACER ASI
# client = PodmanClient(base_url="tcp://localhost:8082")
# repository = PodmanContainerRepository(client)
# service = PodmanContainerService(repository)

#Y EN EL LIST PASSARLO ASI
# @ContainerRouter.get("/containers", response_model=List[PodmanContainerSchema])
# def list_containers(status: Optional[PodmanContainerStatus] = None):
#     try:
#         containers = service.list_containers(status=status if status else PodmanContainerStatus.all)
#         return [PodmanContainerSchema.from_container(container) for container in containers]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@ContainerRouter.get("/containers", response_model=List[PodmanContainerSchema])
def list_containers(
    status: Optional[PodmanContainerStatus] = None,
    service: PodmanContainerService = Depends(get_podman_service)
    #SI QUISIERAMOS QUITAR EL DEPENDS PODRIAMOS HACER
    #    service = PodmanContainerService(repository=PodmanContainerRepository(client=get_podman_client()))

):
    try:
        containers = service.list_containers(status=status if status else PodmanContainerStatus.all)

        return [PodmanContainerSchema.from_container_list(container) for container in containers]
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


    
# @ContainerRouter.post("/v1/Container/containers", response_model=PodmanContainerSchema)
# def create_container(
#     image: str,
#     name: str,
#     command: Optional[List[Any]] = None,
#     repository: PodmanContainerRepository = Depends()
# ):
#     try:
#         container = repository.create(image=image, name=name, command=command)
#         return PodmanContainerSchema(
#             id=container.id,
#             image=str(container.image),
#             name=container.name,
#             status=container.status,
#             labels=container.labels
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#para obtener el contenedor por su id, se llama al metodo fetch_container del servicio, y le pasamos como parametros
#el id del contenedor que queremos obtener y el responsemodel, que es el schema que se encarga de convertir el objeto PodmanContainer
#  a un objeto PodmanContainerSchema, que da el formato correcto a la respuesta
@ContainerRouter.get("/containers/{id_}", response_model=PodmanContainerSchema)
def fetch_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_=id_)
        return PodmanContainerSchema.from_container(container)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#esta funcion sirve para correr un contenedor, tiene unos parametros obligatorios, y otros opcionales
#despues de definir los parametros, se llama al metodo run_container del servicio, que se encarga de correr el contenedor
@ContainerRouter.post("/containers/run", response_model=PodmanContainerSchema)
def run_container(
    image: str,
    name: str,
    environment: Optional[Dict[str, str]] = None,
    labels: Optional[Dict[str, str]] = None,
    command: Optional[List[Any]] = None,
    service: PodmanContainerService = Depends(get_podman_service)
):
    # try:
    #     container = service.run_container(image=image, name=name, environment=environment, labels=labels, command=command)
    #     return PodmanContainerSchema(
    #         id=container.id,
    #         image=str(container.image),
    #         name=container.name,
    #         status=container.status,
    #         labels=container.labels
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    #En lugar de hacer esto, creamos un schema que se encargue de convertir el objeto PodmanContainer a un objeto PodmanContainerSchema
    #lo que sirve para que el schema se encargue de la conversion de los objetos, y no tengamos que hacerlo nosotros
    try:
        container = service.run_container(image=image, name=name, environment=environment, labels=labels, command=command)
        return PodmanContainerSchema.from_container(container)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ContainerRouter.post("/containers/{id_}/copy")
def copy_into_container(
    id_: str,
    source: str,
    destination: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)
        #HACER UNA VERIFICACION DE SI EL CONTENEDOR ES NONE
        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        service.copy_into_container(container, source, destination)
        return {"message": "File copied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Para el start, stop, kill y remove, primero tenemos que obtener el contenedor por su id, y luego llamar al metodo correspondiente del servicio
#para realizar la accion 
@ContainerRouter.post("/containers/{id_}/start")
def start_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)

        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        
        service.start_container(container)
        return {"message": "Container started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ContainerRouter.post("/containers/{id_}/stop")
def stop_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)

        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        service.stop_container(container)
        return {"message": "Container stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ContainerRouter.post("/containers/{id_}/kill")
def kill_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)
        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        service.kill_container(container)
        return {"message": "Container killed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ContainerRouter.post("/containers/{id_}/restart")
def restart_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)
        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        service.restart_container(container)
        return {"message": "Container restarted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ContainerRouter.delete("/containers/{id_}")
def remove_container(
    id_: str,
    service: PodmanContainerService = Depends(get_podman_service)
):
    try:
        container = service.fetch_container(id_)
        if not container:
            raise HTTPException(status_code=404, detail="Container not found")  # Verificar si es None
        service.remove_container(container)
        return {"message": "Container removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ContainerRouter.post("/containers/run_container_secrets", response_model=PodmanContainerSchema)
def run_container_with_secrets(
    image: str,
    name: str,
    environment: Optional[Dict[str, str]] = None,
    labels: Optional[Dict[str, str]] = None,
    command: Optional[List[Any]] = None,
    secrets: Optional[List[str]] = None,
    service: PodmanContainerService = Depends(get_podman_service)
):
    # try:
    #     container = service.run_container(image=image, name=name, environment=environment, labels=labels, command=command)
    #     return PodmanContainerSchema(
    #         id=container.id,
    #         image=str(container.image),
    #         name=container.name,
    #         status=container.status,
    #         labels=container.labels
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    #En lugar de hacer esto, creamos un schema que se encargue de convertir el objeto PodmanContainer a un objeto PodmanContainerSchema
    #lo que sirve para que el schema se encargue de la conversion de los objetos, y no tengamos que hacerlo nosotros
    try:
        container = service.run_container_with_secrets(image=image, name=name, environment=environment, labels=labels, command=command,secrets=secrets)
        return PodmanContainerSchema.from_container(container)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))