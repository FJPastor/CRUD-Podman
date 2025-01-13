
# from contextlib import suppress
# from typing import Any, Dict, Optional
# from podman.domain.manager import PodmanResource


# class Container (PodmanResource):

#     # #Devuelve el nombre del contenedor
#     # @property
#     # def name (self):
#     #     with suppress(KeyError):
#     #         if "Name" in self.attrs:
#     #             return self.attrs["Name"]
#     #         return self.attrs['Names'][0]
#     #     return None
    
#     # #Devuelve el id del contenedor
#     # @property
#     # def id (self):
#     #     with suppress(KeyError):
#     #         if "Id" in self.attrs:
#     #             return self.attrs["Id"]
#     #         return self.attrs['ID']
#     #     return None
    
#     # #Devuelve el estado del contenedor
#     # @property
#     # def status(self):
#     #     """Literal["running", "stopped", "exited", "unknown"]: Returns status of container."""
#     #     with suppress(KeyError):
#     #         return self.attrs["State"]["Status"]
#     #     return "unknown"
    
#     # @property
#     # def ports(self):
#     #     """dict[str, int]: Return ports exposed by container."""
#     #     with suppress(KeyError):
#     #         return self.attrs["NetworkSettings"]["Ports"]
#     #     return {}
    
#     # """Class representing a Podman container."""

#     @property
#     def name(self) -> Optional[str]:
#         """Returns the name of the container."""
#         with suppress(KeyError):
#             if "Name" in self.attrs:
#                 return self.attrs["Name"]
#             return self.attrs['Names'][0]
#         return None

#     @property
#     def id(self) -> Optional[str]:
#         """Returns the ID of the container."""
#         with suppress(KeyError):
#             if "Id" in self.attrs:
#                 return self.attrs["Id"]
#             return self.attrs['ID']
#         return None

#     @property
#     def status(self) -> str:
#         """Returns the status of the container."""
#         with suppress(KeyError):
#             return self.attrs["State"]["Status"]
#         return "unknown"

#     @property
#     def ports(self) -> Dict[str, Any]:
#         """Returns the ports exposed by the container."""
#         with suppress(KeyError):
#             return self.attrs["NetworkSettings"]["Ports"]
#         return {}