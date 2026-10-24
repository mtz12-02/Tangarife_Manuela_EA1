# Sistema de Información – Parqueadero Autos Colombia
## Manuela Tangarife Zapata

## Descripción

Este proyecto consiste en el desarrollo de un sistema de información para el parqueadero Autos Colombia, diseñado para facilitar el registro y control de las operaciones que se realizan diariamente. A través de la aplicación, es posible registrar vehículos, gestionar sus entradas y salidas, asignar celdas de parqueo, registrar novedades y consultar el historial de movimientos.
La solución busca agrupar esta información y facilitar el seguimiento de los vehiculos durante su permanencia en el parqueadero.

## Tecnologías utilizadas

Para el desarrollo del proyecto utilicé las siguientes tecnologías:

- **Python:** lenguaje de programación que escogí he implemente para construir la aplicación.
- **Flask:** framework empleado para gestionar las rutas y funcionalidades del sistema
- **PostgreSQL:** es el sistema gestor de bases de datos encargado de almacenar la información.
- **HTML:** utilizado para presentar las interfaces de la aplicación.
- **psycopg:** biblioteca que permite la conexión entre Python y PostgreSQL.
- **python-dotenv:** herramienta utilizada para cargar la configuración local desde variables de entorno.

## Funcionalidades principales

El sistema cuenta con las siguientes funcionalidades:

- Registro de vehículos y sus datos básicos.
- Registro de entradas con asignación automática de una celda disponible.
- Registro de salidas y liberación de la celda ocupada.
- Registro de novedades asociadas a los movimientos de los vehículos.
- Consulta del historial de entradas, salidas y novedades.
- Visualización del estado general del parqueadero, incluyendo las celdas disponibles y ocupadas.

## Estructura del proyecto

El proyecto está organizado en carpetas y archivos que facilitan la ubicación de sus elementos:

- **`app/`:** contiene el código python de la aplicación y las funciones relacionadas con la conexión a la base de datos.
- **`database/`:** contiene el script SQL para crear las tablas, relaciones y restricciones de la base de datos.
- **`docs/`:** reúne la documentación del proyecto, el informe y el modelo físico de la base de datos.
- **`tests/`:** carpeta destinada a la organización de pruebas del sistema.
- **`requirements.txt`:** contiene las dependencias de Python utilizadas por la aplicación.
- **`.gitignore`:** especifica los archivos y carpetas locales que no deben incluirse en el repositorio.

## Base de datos

La base de datos se llama `autos_colombia` y está desarrollada en PostgreSQL. Su estructura se compone de cuatro tablas principales: `vehiculos`, `celdas`, `movimientos` y `novedades`.
Estas tablas permiten relacionar los vehículos con sus movimientos, identificar las celdas utilizadas y almacenar las novedades que se presenten durante el servicio.
El script de creación se encuentra en la carpeta `database/`, mientras que el modelo físico puede encontrarse en `docs/`.

## Requisitos y configuración

Para ejecutar el sistema se requiere Python 3 y PostgreSQL, además de una base de datos denominada `autos_colombia`.
La conexión utiliza variables de entorno definidas en un archivo local `.env`, donde se configuran los datos de conexión a PostgreSQL. Este archivo es de uso local y no forma parte de los archivos compartidos en el repositorio.

Las dependencias necesarias se encuentran especificadas en `requirements.txt`.

## Ejecución de la aplicación

Una vez preparada la base de datos y configuradas las variables de entorno, la aplicación puede ejecutarse desde la carpeta raíz del proyecto mediante el siguiente comando:

`python app/app.py`

Después de iniciar el servidor, el sistema se puede consultar desde el navegador en `http://127.0.0.1:5000`.
