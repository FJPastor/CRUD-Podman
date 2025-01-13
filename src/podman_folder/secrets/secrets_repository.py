from podman import PodmanClient
from podman.domain.secrets import Secret
from configs.environment import get_environment_variables

env = get_environment_variables()

def get_podman_client():
    # client = PodmanClient(base_url="unix:///var/run/podman/podman.sock")
    client = PodmanClient(base_url="tcp://localhost:8082")

class PodmanSecretRepository:
    def __init__(self, client: PodmanClient):
        self.client = client

    def create_secret(self, secret_name: str, secret_data: str):
        try:
            secret = self.client.secrets.create(secret_name, secret_data.encode())
            return secret
        except Exception as e:
            raise Exception(f"Error creating secret: {str(e)}")



    def get_secret(self, secret_name: str):
        try:
            secret = self.client.secrets.get(secret_name)
            return secret
        except Exception as e:
            raise Exception(f"Error getting secret: {str(e)}")

    def delete_secret(self, secret_name: str):
        try:
            self.client.secrets.remove(secret_name)
        except Exception as e:
            raise Exception(f"Error deleting secret: {str(e)}")

    def list_secrets(self):
        try:
            return self.client.secrets.list()  # Listar todos los secretos
        except Exception as e:
            raise Exception(f"Error listing secrets: {str(e)}")