from collections.abc import Iterator
from typing import Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from podman import PodmanClient

from podman_folder.image.image_schema import PodmanImageSchema
from podman_folder.image.image_service import PodmanImageService
from podman_folder.image.podman_image import PodmanImageRepository
from podman_folder.secrets.secrets_repository import PodmanSecretRepository
from podman_folder.secrets.secrets_schema import PodmanSecretSchema
from podman_folder.secrets.secrets_service import PodmanSecretService



ImageRouter=APIRouter(prefix="/v1/Image", tags=["Images"])

def get_podman_client() -> PodmanClient:
    return PodmanClient(base_url="tcp://localhost:8082")

def get_podman_service() -> PodmanImageService:
    client = get_podman_client()
    repository = PodmanImageRepository(client)
    return PodmanImageService(repository)


@ImageRouter.get("/images",response_model=List[PodmanImageSchema])
def list_images(
    service: PodmanImageService = Depends(get_podman_service)
):
    try:
        images = service.list_images()
        return [PodmanImageSchema.from_image_list(image) for image in images]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)
)
    
# @ImageRouter.post("/images/pull", response_model=Union[PodmanImageSchema, List[PodmanImageSchema]])
# def pull_image(repository: str, tag: str, service: PodmanImageService = Depends(get_podman_service)):
#     try:
#         images = service.pull_image(repository, tag)
#         return [PodmanImageSchema.from_image(image) for image in images] 
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@ImageRouter.post("/pull", response_model=None) # Cambia el modelo de respuesta a None, para poder manejar 2 tipos de respuesta
def pull_image(repository: str, tag: str, service: PodmanImageService = Depends(get_podman_service)):
    try:
        #Llamamos al método pull_image del servicio, que puede devolver una lista de imágenes o un iterador
        images_or_logs = service.pull_image(repository, tag)

        # Si llama a un iterador, usamos StreamingResponse, que da datos de forma progresiva, y espera a que se acabe el iterador
        #util cuando hay procesos largos que devuelven datos de forma progresiva
        if isinstance(images_or_logs, Iterator):
            return StreamingResponse(images_or_logs, media_type="text/plain")  # Streaming logs

        # Si el resultado es una lista de imágenes, las convertimos a su schema
        podman_images = [PodmanImageSchema.from_image(image) for image in images_or_logs]
        return podman_images  # Devolver la lista de imágenes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ImageRouter.post("/images/push")
def push_image(repository: str, tag: str, service: PodmanImageService = Depends(get_podman_service)):
    try:
        result = service.push_image(repository, tag)
        return {"message": "Image pushed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@ImageRouter.get("/images/{name}", response_model=PodmanImageSchema)
def get_image_by_name(name: str, service: PodmanImageService = Depends(get_podman_service)):
    try:
        image = service.get_image_by_name(name)
        return PodmanImageSchema.from_image(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ImageRouter.get("/images/repository/{repository}", response_model=List[PodmanImageSchema])
def list_images_by_repository(repository: str, service: PodmanImageService = Depends(get_podman_service)):
    try:
        images = service.list_images_by_repository(repository)
        return [PodmanImageSchema.from_image_list(image) for image in images]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@ImageRouter.delete("/images/{image}")
def remove_image(image: str, force: Optional[bool] = False, service: PodmanImageService = Depends(get_podman_service)):
    try:
        force = force if force is not None else False
        result = service.remove_image(image, force)
        return {"message": "Image removed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ImageRouter.post("/images/login")
def login(username: str, password: str, registry: str, service: PodmanImageService = Depends(get_podman_service)):
    try:
        service.login_to_registry(username, password, registry)
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @ImageRouter.post("/images/login-with-secrets")
# def login_with_secrets(
#     registry: str,
#     secrets: List[PodmanSecretSchema],  # Recibimos los secretos como un diccionario
#     service: PodmanImageService = Depends(get_podman_service)
# ):
#     try:
#         username = next((secret.name for secret in secrets if secret.id == "your_user_secret_id"), None)
#         password = next((secret.name for secret in secrets if secret.id == "your_password_secret_id"), None)
#         if not username or not password:
#             raise HTTPException(status_code=400, detail="Invalid secrets provided")

#         service.login_to_registry(username=username, password=password, registry=registry)
#         return {"message": "Login successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @ImageRouter.post("/images/login-with-secrets")
# def login_with_secrets(secret_name_user: str, secret_name_pass: str, registry: str, service: PodmanImageService = Depends(get_podman_service)):
#     try:
#         service.login_with_secrets(secret_name_user, secret_name_pass, registry)
#         return {"message": "Login successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @ImageRouter.post("/images/login-with-secrets")
# def login_with_secrets(secret_name_user: str, secret_name_pass: str, registry: str, service: PodmanImageService = Depends(get_podman_service)):
#     try:
#         service.login_with_secrets(secret_name_user, secret_name_pass, registry)
#         return {"message": "Login successful"}
#     except Exception as e:
#         logger.error(f"Error en el router durante el login: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# @ImageRouter.post("/images/login-with-secrets")
# def login_with_secrets(
#     secret_name_user: str,
#     secret_name_pass: str,
#     registry: str,
#     secret_service: PodmanSecretService = Depends()
# ):
#     try:
#         # Obtener el contenido de los secretos
#         user_secret = secret_service.get_secret(secret_name_user)
#         pass_secret = secret_service.get_secret(secret_name_pass)

#         # Realizar el login utilizando los secretos obtenidos
#         # Aquí debes ajustar el código para utilizar user_secret y pass_secret en el login
#         # Por ejemplo:
#         login_result = login_with_secrets(user_secret, pass_secret, registry)

#         return {"message": "Login successful", "result": login_result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error al obtener o decodificar los secretos: {str(e)}")