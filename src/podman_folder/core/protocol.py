from typing import Protocol,Iterable
from podman import PodmanClient
from podman.domain.containers import Container
from podman.domain.images import Image

class PodmanImageRepo(Protocol):
     def pull(self, client: PodmanClient, repository: str, tag: str) -> Iterable[Image]:
        ...