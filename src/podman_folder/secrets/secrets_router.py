from typing import List
from fastapi import APIRouter, Depends, HTTPException
from podman import PodmanClient

from podman_folder.secrets.secrets_repository import PodmanSecretRepository
from podman_folder.secrets.secrets_schema import PodmanSecretSchema
from podman_folder.secrets.secrets_service import PodmanSecretService

SecretRouter = APIRouter(prefix="/v1/Secret", tags=["Secrets"])



def get_podman_client() -> PodmanClient:
    return PodmanClient(base_url="tcp://localhost:8082")

def get_podman_service() -> PodmanSecretService:
    client = get_podman_client()
    repository = PodmanSecretRepository(client)
    return PodmanSecretService(repository)



@SecretRouter.post("/secrets", response_model=PodmanSecretSchema)
def create_secret(secret_name: str, secret_data: str, service: PodmanSecretService = Depends(get_podman_service)):
    try:
        secret = service.create_secret(secret_name, secret_data)
        return PodmanSecretSchema.from_secret(secret)  # Usar el método del esquema para convertir a respuesta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@SecretRouter.get("/secrets/{secret_name}", response_model=PodmanSecretSchema)
def get_secret(secret_name: str, service: PodmanSecretService = Depends(get_podman_service)):
    try:
        secret = service.get_secret(secret_name)
        return PodmanSecretSchema.from_secret(secret)  # Usar el método del esquema para convertir a respuesta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@SecretRouter.get("/secrets", response_model=List[PodmanSecretSchema])
def list_secrets(service: PodmanSecretService = Depends(get_podman_service)):
    try:
        secrets = service.list_secrets()
        return [PodmanSecretSchema.from_secret(secret) for secret in secrets]  # Convertir a lista de esquemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@SecretRouter.delete("/secrets/{secret_name}")
def delete_secret(secret_name: str, service: PodmanSecretService = Depends(get_podman_service)):
    try:
        service.delete_secret(secret_name)
        return {"message": f"Secret '{secret_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
