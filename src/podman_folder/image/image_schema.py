from pydantic import BaseModel
from typing import Optional

class PodmanImageSchema(BaseModel):
    id: Optional[str]
    name: Optional[str]
    tag: Optional[str]
    size: Optional[int]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_image_list(cls, image): 
        return cls(
            id=image.attrs['Id'],
            name=image.attrs['RepoTags'][0] if image.attrs.get('RepoTags') else None,
            tag=image.attrs['RepoTags'][1] if image.attrs.get('RepoTags') and len(image.attrs['RepoTags']) > 1 else None,
            size=image.attrs['Size']
        )

    # @classmethod
    # def from_image(cls,image):
    #     print("Image attributes:", image.attrs)
    #     name= image.attrs.get('Name', None)
    #     tag = None
    #     if image.attrs.get('RepoTags') and len(image.attrs['RepoTags']) > 1:
    #         tag = image.attrs['RepoTags'][1]
    #     return cls(
    #         id=image.attrs['Id'],
    #         name=name,
    #         tag=image.attrs['RepoTags'][0] if image.attrs.get('RepoTags') else None,
    #         size=image.attrs['Size']
    #     )

    @classmethod
    def from_image(cls, image):
        print("Image attributes:", image.attrs)  # Para depuración, ver los atributos reales de la imagen
        name = None
        tag = None

        # Validar si RepoTags está presente y contiene al menos un elemento
        if image.attrs.get('RepoTags'):
            name = image.attrs['RepoTags'][0]
            if len(image.attrs['RepoTags']) > 1:
                tag = image.attrs['RepoTags'][1]

        return cls(
            id=image.attrs.get('Id'),
            name=name,
            tag=tag,
            size=image.attrs.get('Size')  # Manejar si Size está ausente
        )
