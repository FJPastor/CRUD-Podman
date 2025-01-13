from pydantic import BaseModel
from typing import Optional, Dict, Any

class PodmanSecretSchema(BaseModel):
    id: Optional[str]
    name: Optional[str]
    # Puedes agregar otros campos si es necesario

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_secret(cls, secret):
        return cls(
            id=secret.id,
            name=secret.name,
        )
