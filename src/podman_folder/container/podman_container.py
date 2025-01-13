from enum import Enum
from fastapi import Depends, HTTPException
from podman import PodmanClient #esto crea una instancia de podman.client.Client, sirve para interactuar con podman y hacer llamadas a la API de podman
from typing import Dict, Generator, Iterable, Any, List, Optional, Union, Iterator
import tarfile
from loguru import logger
from podman.errors import APIError
import os
from configs.environment import get_environment_variables
# from configs import 

from podman.domain.containers import Container as PodmanContainer

from podman_folder.container.container_schema import PodmanContainerSchema
from podman_folder.model import PodmanFilter



#puedo implementar en el .env la variable de entorno para el base_url,
#y en el get_environment_variables() puedo obtener el valor de la variable de entorno
env = get_environment_variables()
#pero finalmente lo que hago es poner el valor directamente en el base_url
#IMPORTANTE ejecutar en linea de comandos: podman system service -t 0 tcp:localhost:8082
#para mantener el servicio de podman activo escuchando en el puerto 8082
def get_podman_client():
    client = PodmanClient(base_url="tcp://localhost:8082")


class PodmanContainerRepository:

        # def __init__(self, client: PodmanClient = Depends(get_podman_client)): ESTO ME ESTABA DANDO ERROR
        # self.client = client

        #Con este init no hace falta pasar el cliente como argumento, ya que se inicializa en el constructor
    def __init__(self, client: PodmanClient):
        self.client = client

    def list(self, all_: bool = False, filters: Optional[PodmanFilter] = None) -> Iterable[PodmanContainer]:
        filters_dict = filters.to_dict() if filters else {}
        try:
            containers = self.client.containers
            cc=containers.list(all=all_, filters=filters_dict)
            return cc
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")



    def create(self, image: str, name: str, command: Optional[List[Any]] = None) -> PodmanContainer:
        try:
            return self.client.containers.create(image=image, name=name, command=command)
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


    # def fetch(self, client: PodmanClient, id_: str) -> PodmanContainer: Listamos el cliente como argumento, pero no lo usamos
    #porque ya esta inicializado en el constructor, por lo que lo usaríamos como self.client para acceder a el
    #     return client.containers.get(id_)
    #por lo que lo cambiamos a self.client y quitamos el argumento client

    def fetch(self, id_: str) -> PodmanContainer:
        try:
            return self.client.containers.get(id_)
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    
    #En el metodo run, se puede pasar un diccionario con las variables de entorno y un diccionario con las etiquetas
    # y un comando opcional    
    def run(self, image: str, name: str, environment=None, labels=None, command: Optional[List[Any]] = None) -> PodmanContainer:
        try:
            container = self.client.containers.run( #definimos el contenedor y le añadimos los parametros, las label y los comandos son opcionales
                #y se pasan como diccionarios vacios si no se pasan como argumentos
                #Un diccionario es un conjunto de pares clave-valor, donde la clave es unica y no puede repetirse
                #y sirven para almacenar datos de forma estructurada, en este caso se usan para pasar las variables de entorno y las etiquetas
                image=image,
                name=name,
                environment=environment if environment else {}, #se añaden las variables de entorno para dar configuracion al contenedor
                labels=labels if labels else {}, #se añaden las etiquetas al contenedor
                detach=True, #se ejecuta en segundo plano
                command=command if command else [], #ejecuta el comando en el contenedor
                restart_policy={"Name": "on-failure"} #se reinicia el contenedor si falla
            )
            if isinstance(container, PodmanContainer): #si el contenedor es una instancia de PodmanContainer
                return container
            else:
                raise TypeError("Se esperaba un PodmanContainer, se recibe {}".format(type(container))) 
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


    #En el metodo copy_into_container, se copia un archivo en el contenedor, se pasa el contenedor, la ruta del archivo
    def copy_into_container(self, container: PodmanContainer, source: str, destination: str):
        with tarfile.open("aux.tar", "w:gz") as tar:
            tar.add(source, arcname=os.path.relpath(source, start=os.path.dirname(source)))
        with open("aux.tar", 'rb') as file:
            ok = container.put_archive(path=destination, data=file.read())
            os.remove("aux.tar")
            if not ok:
                raise Exception('Put file failed')
            else:
                logger.info("CONTAINER | run | config file inserted")

    #En el metodo start, se inicia el contenedor
    def start(self, container: PodmanContainer) -> Any:
        return container.start()
    #En el metodo stop, se para el contenedor
    def stop(self, container: PodmanContainer) -> Any:
        return container.stop()
    #En el metodo kill, se mata el contenedor, en caso de que no se pueda parar
    def kill(self, container: PodmanContainer) -> Any:
        return container.kill()
    #En el metodo restart, se reinicia el contenedor
    def restart(self, container: PodmanContainer) -> Any:
        return container.restart()
    #En el metodo remove, se borra el contenedor
    def remove(self, container: PodmanContainer) -> Any: #Si le pongo ,force=True, hace kill antes de borrar
        return container.remove()

    def run_container_secrets(self,image: str,name: str,environment=None,labels=None,command: Optional[List[Any]] = None,secrets: Optional[List[str]] = None) -> PodmanContainer:
        try:
            # Utilizamos el parámetro secrets en la configuración del contenedor
            container = self.client.containers.run(
                image=image,
                name=name,
                environment=environment if environment else {},
                labels=labels if labels else {},
                detach=True,
                command=command if command else [],
                restart_policy={"Name": "on-failure"},
                secrets=secrets if secrets else []  # Añadimos los secretos
            )
            if isinstance(container, PodmanContainer):
                return container
            else:
                raise TypeError("Se esperaba un PodmanContainer, se recibe {}".format(type(container)))
        except APIError as e:
            raise HTTPException(status_code=500, detail=f"Podman API error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
        
        #Este metodo se usa para crear un contenedor con secretos, se le pasa el nombre de la imagen, el nombre del contenedor, los secretos,
        #  las variables de entorno, las etiquetas y el comando a ejecutar, si queremos que una variable de entorno use un secreto,
        #  se le pasa el nombre del secreto en el valor de la variable de entorno
        #Por ejemplo siendo la API_KEY el nombre del secreto, si queremos que la variable de entorno API_KEY tenga el valor del secreto,
        #  se le pasa el valor de la variable de entorno como API_KEY
        #Siendo la API
            #         {
            # "environment": {
            #     "additionalProp1": "string",
            #     "additionalProp2": "string",
            #     "additionalProp3": "string"
            # },
            # "labels": {
            #     "additionalProp1": "string",
            #     "additionalProp2": "string",
            #     "additionalProp3": "string"
            # },
            # "command": [
            #     "command"
            # ],
            # "secrets": [
            #     "secret"
            # ]
            # }
    #para usar el secret como variable de entorno, se le pasa el nombre del secreto en el valor de la variable de entorno
    #quedando la API asi:
            #         {
            # "environment": {
            #    "API_KEY": "API_KEY" #se le pasa el nombre del secreto en el valor de la variable de entorno
            # },
            # "labels": {
            #    "additionalProp1": "string",
            #   "additionalProp2": "string",
            #  "additionalProp3": "string"
            # },
            # "command": [
            #    "command"
            # ],
            # "secrets": [
            #   "API_KEY" aqui usariamos API_KEY, que es el nombre del secreto
            #
            # ]
            #   