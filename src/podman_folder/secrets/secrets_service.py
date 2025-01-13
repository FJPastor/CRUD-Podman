from podman_folder.secrets.secrets_repository import PodmanSecretRepository

class PodmanSecretService:
    def __init__(self, repository: PodmanSecretRepository):
        self.repository = repository

    def create_secret(self, secret_name: str, secret_data: str):
        return self.repository.create_secret(secret_name, secret_data)

    def get_secret(self, secret_name: str):
        return self.repository.get_secret(secret_name)

    def list_secrets(self):
        return self.repository.list_secrets()

    def delete_secret(self, secret_name: str):
        return self.repository.delete_secret(secret_name)
