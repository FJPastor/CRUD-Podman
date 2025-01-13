from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from configs.database import Engine

# Base Entity Model Schema
EntityMeta = declarative_base()


def init():
   # EntityMeta.metadata.create_all(bind=Engine)
    # Crea un inspector de la base de datos
    inspector = inspect(Engine)

    # Verifica si la tabla  ya existe
    if not inspector.has_table("Departamento"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
    if not inspector.has_table("Departamento_Idioma"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
    if not inspector.has_table("Empleado"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
    if not inspector.has_table("EstadoProceso"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
    if not inspector.has_table("ReglaAsignacion"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
    if not inspector.has_table("Tarea"):
        EntityMeta.metadata.create_all(bind=Engine)  # Crea las tablas solo si no existen
