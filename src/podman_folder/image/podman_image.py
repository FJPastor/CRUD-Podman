
from collections.abc import Iterator
from typing import Any, Dict, Iterable, List, Literal, Optional, Union
from podman import PodmanClient
from configs.environment import get_environment_variables
from podman.domain.images import Image
from podman.errors import APIError
from fastapi import Depends, HTTPException


env = get_environment_variables()

def get_podman_client():
    # client = PodmanClient(base_url="unix:///var/run/podman/podman.sock")
    client = PodmanClient(base_url="tcp://localhost:8082")

class PodmanImageRepository:
        
    def __init__(self, client: PodmanClient):
        self.client = client  # Guardamos el cliente en una variable de instancia

    #esta funcion sirve para loguearse en un registro de imagenes
    def login(self, username: str, password: str, registry: str,reauth:bool=False) -> None:
        self.client.login(username=username, password=password, registry=registry,reauth=reauth)
#Codigo de podman:
    # def login(
    #     self,
    #     username: str,
    #     password: Optional[str] = None,
    #     email: Optional[str] = None,
    #     registry: Optional[str] = None,
    #     reauth: Optional[bool] = False,  # pylint: disable=unused-argument #si es true refresca la autenticacion existente, sirve para cuando la autenticacion caduca
    #     dockercfg_path: Optional[str] = None,  # pylint: disable=unused-argument
    # ) -> Dict[str, Any]:
    #     """Log into Podman service.

    #     Args:
    #         username: Registry username
    #         password: Registry plaintext password
    #         email: Registry account email address
    #         registry: URL for registry access. For example,
    #         reauth: Ignored: If True, refresh existing authentication. Default: False
    #         dockercfg_path: Ignored: Path to custom configuration file.
    #             https://quay.io/v2
    #     """
#A diferencia de docker, en podman no puede ser solo un iterator, ya que puede devolver un objeto, una lista de objetos o un iterador
#lo que implicaria que el tipo de retorno sea una union de estos tres tipos
    def pull(self, repository: str, tag: str) -> Union[Image, List[Image], Iterator[str]]:
        images = self.client.images.pull(repository, tag)
        return images
    
    def push(self, repository: str, tag: str) -> Union[str, Iterator[Union[str, Dict[str, Any]]]]:
        return self.client.images.push(repository, tag) #pushea al repositorio la imagen con el tag especificado

    def list(self, all_: bool = False, filters: Optional[Dict] = None) -> Iterable[Image]:
        filters = filters if filters else {}
        try:
            images = self.client.images.list(all=all_, filters=filters)
            return images
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    
    def getByName(self, name: str) -> Image:
        image = self.client.images.get(name=name) #usamos el metodo get del cliente de Podman para obtener la imagen con el nombre que queramos
        return image

#Crei que con un list podia filtar por nombre, pero el nombre que se le pasa es el del repositorio, por lo que devuelvo una lista de imagenes
#que tengan el mismo nombre de repositorio, mientras que get devuelve una imagen con el nombre especificado
    def listByRepository(self, repository: str) -> Iterable[Image]:
        images = self.client.images.list(repository=repository)
        return images
    


    #Para eliminar una imagen se le pasa nombre o id y como opcional un booleano que indica si se quiere forzar la eliminacion
    def remove(self, image: str, force: Optional[bool]=False) -> List[Dict[Literal["Deleted","Untagged","Errors","ExitCode"],Union[str, int]]]:
        return self.client.images.remove(image=image)
    
    def login_with_secrets(self, username: str, password: str, registry: str, reauth: bool = False) -> None:
        self.client.login(username=username, password=password, registry=registry, reauth=reauth)

