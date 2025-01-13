import base64
from collections.abc import Iterator
from typing import Any, Dict, Iterable, List, Union
from fastapi import HTTPException
import logging
from podman_folder.image.podman_image import PodmanImageRepository
from podman.domain.images import Image as PodmanImage  # Cambia el nombre para evitar confusión
# from podman_folder.model import PodmanImage  # Apunto directamente a el domain de Podman en lugar de al model, no es necesario el model 
from podman_folder.image.image_schema import PodmanImageSchema
from podman_folder.model import PodmanFilter
# from podman_folder.secrets.secrets_service import PodmanSecretService
from podman.domain.secrets import Secret
from podman.domain.secrets import SecretsManager

# logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

class PodmanSecretService:
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets_manager = secrets_manager

    # def get_secret(self, secret_name: str) -> Secret:
    #     """Obtiene un secreto dado su nombre."""
    #     return self.secrets_manager.get(secret_name)


class PodmanImageService:
    # def __init__(self, repository: PodmanImageRepository):
    #     self.repository = repository

    def __init__(self, repository: PodmanImageRepository):
        self.repository = repository

    def login_to_registry(self, username: str, password: str, registry: str, reauth: bool = False) -> None:
        logger.info(f"Logging into registry: {registry} with username: {username} and password: {'*' * len(password)}")
        try:
            self.repository.login(username=username, password=password, registry=registry, reauth=reauth)
        except Exception as e:
            logger.error(f"Error logging into registry: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def list_images(self) -> Iterable[PodmanImage]:
        logger.info("Listing all images")
        filter = PodmanFilter()  # Crea un filtro vacío
        try:
            all_images=True
            images = self.repository.list(all_=all_images)  
            return images
        except Exception as e:
            logger.error(f"Error listing images: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_image_by_name(self, name: str) -> PodmanImage: 
        logger.info(f"Getting image by name: {name}")
        try:
            image = self.repository.getByName(name=name) #aplicamos el metodo getByName del repositorio 
            return image 
        except Exception as e:
            logger.error(f"Error getting image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def remove_image(self, name: str, force: bool = False) -> None:
        logger.info(f"Removing image: {name}, force: {force}")
        try:
            self.repository.remove(image=name, force=force)  
        except Exception as e:
            logger.error(f"Error removing image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    

    def list_images_by_repository(self, repository: str) -> Iterable[PodmanImage]:
        logger.info(f"Listing images by repository: {repository}")
        try:
            # Sacamos todas las imagenees
            images = self.repository.list()  
            # filtra tomando el nombre del repositorio y lo compara con el nombre de la imagen, si empieza igual, lo guarda en la lista
            repo_filtro = [image for image in images if image.tags and any(tag.startswith(repository) for tag in image.tags)]
            return repo_filtro
        except Exception as e:
            logger.error(f"Error listing images: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def pull_image(self, repository: str, tag: str) -> Union[List[PodmanImage], Iterator[str]]:
        logger.info(f"Pulling image from repository: {repository}, tag: {tag}")
        try:
            images = self.repository.pull(repository=repository, tag=tag)

            #El pull de podman puede devolver un objeto, una lista de objetos o un iterador, por lo que tenemos que identificar el tipo de retorno
            #Aqui verificamos si es un iterador, si es asi, devolvemos un StreamingResponse en el router
            if isinstance(images, Iterator):
                return images  

            # Si lo que devuelve es una sola imagen, la convertimos en una lista de una sola imagen
            #y en el router la convertimos a su schema 
            if isinstance(images, PodmanImage):
                return [images]  

            #Si es una lista de imagenes, la devolvemos como tal
            return images  
        except Exception as e:
            logger.error(f"Error pulling image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


    def push_image(self, repository: str, tag: str) -> Union[str, Iterator[Union[str, Dict[str, Any]]]]:
        logger.info(f"Pushing image to repository: {repository}, tag: {tag}")
        try:
            return self.repository.push(repository=repository, tag=tag)
        except Exception as e:
            logger.error(f"Error pushing image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
    #Intente hacer un login con secrets, pero no sale bien porque van encriptados y no se puede acceder a ellos a desencriptarlos

    # def login_to_registry_with_secrets(self, registry: str, secrets: Dict[str, str], reauth: bool = False) -> None:
    #     logger.info(f"Logging into registry: {registry} with secrets.")
    #     try:
    #         self.repository.login_with_secrets(registry=registry, secrets=secrets, reauth=reauth)
    #     except Exception as e:
    #         logger.error(f"Error logging into registry with secrets: {str(e)}")
    #         raise HTTPException(status_code=500, detail=str(e))

    # def login_with_secrets(self, secret_name_user: str, secret_name_pass: str, registry: str, reauth: bool = False) -> None:
    #     # Obtiene el secreto del nombre proporcionado
    #     user_secret = self.secret_service.get_secret(secret_name_user)
    #     pass_secret = self.secret_service.get_secret(secret_name_pass)

    #     # Verifica que se hayan obtenido los secretos
    #     if not user_secret or not pass_secret:
    #         error_message = "Error al obtener secretos"
    #         logger.error(error_message)
    #         raise HTTPException(status_code=404, detail=error_message)
        
    #     # Loggear los secretos obtenidos (solo loggear el nombre, no el contenido por seguridad)
    #     logger.info(f"Obtenido el secreto de usuario: {secret_name_user}")
    #     logger.info(f"Obtenido el secreto de contraseña: {secret_name_pass}")

    #     # Loggear la URL del registro
    #     logger.info(f"Intentando hacer login en el registro: {registry}")

    #     # Verificar el contenido de los secretos
    #     logger.debug(f"Contenido del secreto de usuario: {user_secret}")
    #     logger.debug(f"Contenido del secreto de contraseña: {pass_secret}")

    #     # Realiza el login utilizando el contenido de los secretos
    #     try:
    #         self.repository.login(
    #             username=user_secret.name,  # Asumiendo que 'name' contiene el usuario
    #             password=pass_secret.name,   # Asumiendo que 'name' contiene la contraseña
    #             registry=registry,
    #             reauth=reauth
    #         )
    #         logger.info(f"Login exitoso en el registro {registry} con usuario {secret_name_user}")
    #     except Exception as e:
    #         logger.error(f"Error durante el login: {e}")
    #         raise HTTPException(status_code=500, detail=f"Error durante el login: {str(e)}")
    # def login_with_secrets(self, secret_name_user: str, secret_name_pass: str, registry: str, reauth: bool = False) -> None:
    #     # Obtiene el secreto del nombre proporcionado
    #     # user_secret = self.secret_service.get_secret(secret_name_user)
    #     # pass_secret = self.secret_service.get_secret(secret_name_pass)
    #     logger.info(f"Obteniendo secreto: {secret_name_user}")
    #     user_secret = self.secret_service.get_secret(secret_name_user)
    #     logger.info(f"Secreto de usuario obtenido: {user_secret}")

    #     logger.info(f"Obteniendo secreto: {secret_name_pass}")
    #     pass_secret = self.secret_service.get_secret(secret_name_pass)
    #     logger.info(f"Secreto de contraseña obtenido: {pass_secret}")

    #     # Verifica que se hayan obtenido los secretos
    #     if not user_secret or not pass_secret:
    #         error_message = "Error al obtener secretos"
    #         logger.error(error_message)
    #         raise HTTPException(status_code=404, detail=error_message)

    #     # Loggear los secretos obtenidos (solo loggear el nombre, no el contenido por seguridad)
    #     logger.info(f"Obtenido el secreto de usuario: {secret_name_user}")
    #     logger.info(f"Obtenido el secreto de contraseña: {secret_name_pass}")

    #     # Obtener el contenido de los secretos a través de la API
    #     try:
    #         logger.debug(f"Contenido del secreto de usuario: {user_secret.attrs}")
    #         logger.debug(f"Contenido del secreto de contraseña: {pass_secret.attrs}")
    #         logger.debug(f"Estructura del secreto de usuario: {user_secret.attrs}")
    #         logger.debug(f"Estructura del secreto de contraseña: {pass_secret.attrs}")


    #         # Acceder al contenido de los secretos
    #         decoded_user = user_secret.attrs['Spec'].get('Data', None)
    #         decoded_pass = pass_secret.attrs['Spec'].get('Data', None)
    #         if decoded_user is None or decoded_pass is None:
    #             raise HTTPException(status_code=404, detail="Secret data not found.")
                
    #         decoded_user = base64.b64decode(decoded_user).decode('utf-8')
    #         decoded_pass = base64.b64decode(decoded_pass).decode('utf-8')

    #         # Loggear el usuario y la longitud de la contraseña por seguridad
    #         logger.debug(f"Usuario decodificado: {decoded_user}")
    #         logger.debug(f"Longitud de la contraseña decodificada: {len(decoded_pass)}")
    #     except Exception as e:
    #         logger.error(f"Error al obtener o decodificar los secretos: {e}")
    #         raise HTTPException(status_code=500, detail=f"Error al obtener o decodificar los secretos: {str(e)}")

    #     # Loggear la URL del registro
    #     logger.info(f"Intentando hacer login en el registro: {registry}")

    #     # Realiza el login utilizando el contenido de los secretos decodificados
    #     try:
    #         self.repository.login(
    #             username=decoded_user,  # Usar el valor decodificado
    #             password=decoded_pass,   # Usar el valor decodificado
    #             registry=registry,
    #             reauth=reauth
    #         )
    #         logger.info(f"Login exitoso en el registro {registry} con usuario {secret_name_user}")
    #     except Exception as e:
    #         logger.error(f"Error durante el login: {e}")
    #         raise HTTPException(status_code=500, detail=f"Error durante el login: {str(e)}")