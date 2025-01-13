from fastapi import Depends, FastAPI
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter
import uvicorn
from configs.environment import get_environment_variables
# from configs.database.GraphQL import get_graphql_context
from metadata.tags import Tags
from models.base_model import init
from routers.v1.estadoProceso_router import EstadoProcesoRouter
from routers.v1.departamentoIdioma_router import DepartamentoIdiomaRouter
from routers.v1.empleado_router import EmpleadoRouter
from routers.v1.departamento_router import DepartamentoRouter
from routers.v1.tarea_router import TareaRouter
from routers.v1.reglaAsignacion_router import ReglaAsignacionRouter
# from schemas.graphql.Query import Query
# from schemas.graphql.Mutation import Mutation
from loguru import logger
from podman_folder.container.podman_container import PodmanContainerRepository
from podman import PodmanClient
from podman_folder.container_router import ContainerRouter
from podman_folder.image.image_router import ImageRouter
from podman_folder.secrets.secrets_router import SecretRouter


# Application Environment Configuration
env = get_environment_variables()


# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
    docs_url="/api/docs",
)

# Add Routers
app.include_router(EstadoProcesoRouter)
app.include_router(DepartamentoIdiomaRouter)
app.include_router(EmpleadoRouter)
app.include_router(DepartamentoRouter)
app.include_router(TareaRouter)
app.include_router(ReglaAsignacionRouter)
app.include_router(ContainerRouter) 
app.include_router(ImageRouter) 
app.include_router(SecretRouter) 

# GraphQL Schema and Application Instance
# schema = Schema(query=Query, mutation=Mutation)
# graphql = GraphQLRouter(
#     schema,
#     graphiql=env.DEBUG_MODE,
#     context_getter=get_graphql_context,
# )

# # Integrate GraphQL Application to the Core one
# app.include_router(
#     graphql,
#     prefix="/graphql",
#     include_in_schema=False,
# )

# Initialise Data Model Attributes
init()

#HARDCODEADO AQUI, POR ESO NO FALLA Q NO LE PASE LAS VARIABLES DE ENTORNO CORRECTAMENTE
def start_web_server() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="debug",
        log_config=None
    )

start_web_server()
