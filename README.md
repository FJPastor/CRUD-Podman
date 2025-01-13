# Project Documentation

## Overview
This project provides CRUD operations on databases and integrates Podman for local container operations via Swagger.

## Podman Configuration

### API Setup
To use the Podman API, start the service on port 8082 with:


podman system service -t 0 tcp:localhost:8082


### Database Container
Create a MySQL database container using:


podman run -e MYSQL_ROOT_PASSWORD=root -p 8081:3306 -d docker.io/library/mysql:latest


## Database Schema

### Department Tables

"sql"
CREATE TABLE Master.Departamento (
    id SMALLINT UNSIGNED NOT NULL,
    nombre VARCHAR(255),
    CONSTRAINT unique_id_departamento UNIQUE (id)
);

CREATE TABLE Master.Departamento_Idioma (
    id SMALLINT UNSIGNED NOT NULL,
    codDepartamento SMALLINT UNSIGNED,
    codIdioma SMALLINT UNSIGNED,
    nombre VARCHAR(255),
    CONSTRAINT unique_id_departamento_idioma UNIQUE (id),
    CONSTRAINT fk_departamento FOREIGN KEY (codDepartamento) 
    REFERENCES Master.Departamento(id)
);


### Process Status Table

sql
CREATE TABLE Master.EstadoProceso (
    id SMALLINT UNSIGNED NOT NULL,
    nombre VARCHAR(255),
    CONSTRAINT unique_id_estado_proceso UNIQUE (id)
);


### Employee Table

sql
CREATE TABLE Master.Empleado (
    id SMALLINT UNSIGNED NOT NULL,
    codInstalacion SMALLINT UNSIGNED,
    codDepartamento SMALLINT UNSIGNED,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    codigoEmpleado VARCHAR(255),
    fechaAlta DATE,
    fechaBaja DATE,
    ubicacion VARCHAR(255),
    codEstado SMALLINT UNSIGNED,
    CONSTRAINT unique_id_empleado UNIQUE (id),
    CONSTRAINT fk_estado_proceso_empleado FOREIGN KEY (codEstado) 
    REFERENCES Master.EstadoProceso(id),
    CONSTRAINT fk_departamento_empleado FOREIGN KEY (codDepartamento) 
    REFERENCES Master.Departamento(id)
);


### Task Table

sql
CREATE TABLE Master.Tarea (
    id SMALLINT UNSIGNED NOT NULL,
    codEmpleado SMALLINT UNSIGNED,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    detalles JSON,
    prioridad VARCHAR(255),
    duracionEstimada VARCHAR(40),
    recursos JSON,
    responsable VARCHAR(255),
    estado TINYINT(1),
    comentario VARCHAR(255),
    CONSTRAINT unique_id_tarea UNIQUE (id),
    CONSTRAINT fk_tarea_empleado FOREIGN KEY (codEmpleado) 
    REFERENCES Master.Empleado(id)
);


### Assignment Rules Table

sql
CREATE TABLE Master.ReglaAsignacion (
    id SMALLINT UNSIGNED NOT NULL,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    origen INT UNSIGNED,
    destino INT UNSIGNED,
    codTareaOrigen SMALLINT UNSIGNED,
    codTareaDestino SMALLINT UNSIGNED,
    CONSTRAINT unique_id_regla_asignacion UNIQUE (id),
    CONSTRAINT fk_tarea_origen FOREIGN KEY (codTareaOrigen) 
    REFERENCES Master.Tarea(id),
    CONSTRAINT fk_tarea_destino FOREIGN KEY (codTareaDestino) 
    REFERENCES Master.Tarea(id),
    CONSTRAINT unique_origen UNIQUE (origen, codTareaOrigen),
    CONSTRAINT diferente_origen_destino CHECK (codTareaDestino <> codTareaOrigen)
);


## Sample Data

### Process Status Data

sql
INSERT INTO Master.EstadoProceso (id, nombre) VALUES (1, 'Activo');


### Department Data

sql
INSERT INTO Master.Departamento (id, nombre) 
VALUES (1, 'Recursos Humanos');

INSERT INTO Master.Departamento_Idioma (id, codDepartamento, codIdioma, nombre) 
VALUES (1, 1, 1, 'Human Resources');


### Employee Data

sql
INSERT INTO Master.Empleado (
    id, codInstalacion, codDepartamento, nombre, descripcion, 
    codigoEmpleado, fechaAlta, fechaBaja, codEstado, ubicacion
) VALUES 
(1, 19, 1, 'Juan Pérez', 'Empleado Senior', '70A741CD7B06', 
    '2024-10-04', NULL, 1, 'Oficina Central'),
(2, 20, 1, 'María López', 'Asistente', 'abcdefghi', 
    '2024-10-04', NULL, 1, 'Sucursal 2');


### Task Data

sql
INSERT INTO Master.Tarea (
    id, codEmpleado, nombre, descripcion, detalles, prioridad, 
    duracionEstimada, recursos, responsable, estado, comentario
) VALUES 
(1, 1, 'Tarea A', 'Descripción de la Tarea A', '["Paso 1", "Paso 2"]', 
    'Alta', '4 horas', '["Recurso A", "Recurso B"]', 'Juan Pérez', 1, 'Sin problemas'),
(2, 2, 'Tarea B', 'Descripción de la Tarea B', '["Paso 1", "Paso 2"]', 
    'Media', '2 horas', '["Recurso X"]', 'María López', 0, 'En espera');


### Assignment Rules Data

sql
INSERT INTO Master.ReglaAsignacion (
    id, nombre, descripcion, origen, destino, codTareaOrigen, codTareaDestino
) VALUES 
(1, 'Regla 1', 'Regla de asignación entre tareas', 8080, 8081, 1, 2),
(2, 'Regla 2', 'Regla de retorno', 8081, 8080, 2, 1);
