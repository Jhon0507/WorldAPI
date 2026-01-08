# World API - FastAPI & MariaDB

Una API REST profesional construida con **Python** y **FastAPI** para gestionar una base de datos geográfica mundial (`world`). Permite realizar operaciones CRUD completas sobre Ciudades, Países e Idiomas.

## Características

* **Tecnología Moderna:** Backend asíncrono y veloz con FastAPI.
* **Base de Datos Relacional:** Integración con MariaDB/MySQL usando SQLAlchemy.
* **Validación Robusta:** Uso de Pydantic V2 para asegurar la integridad de los datos.
* **CRUD Completo:**
    * Create, Read, Update, Delete para **Ciudades**.
    * Gestión de **Países** con códigos ISO de 3 letras.
    * Manejo de **Idiomas** con claves primarias compuestas.
* **Documentación Automática:** Swagger UI y ReDoc integrados.

---

## Requisitos Previos

* Python 3.10 o superior.
* Servidor MariaDB o MySQL corriendo localmente.
* Base de datos `world` importada (archivo `.sql`).

---

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clonar el proyecto
Descarga el código fuente en tu máquina local.

### 2. Crear entorno virtual (Recomendado)
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
````
### 3. Instalar dependencias
Instala las librerías necesarias (FastAPI, Uvicorn, SQLAlchemy, Pydantic, etc.) ejecutando:

```bash
pip install -r requirements.txt
````

### 4. Configurar Base de Datos
* Asegúrate de tener tu servidor MariaDB o MySQL encendido (por ejemplo, mediante XAMPP).
* Abre el archivo database.py.
* Modifica la variable SQLALCHEMY_DATABASE_URL con tu usuario y contraseña:

````bash
# Formato: mysql+pymysql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_DB
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3306/world"
````

### 5. Ejecución

````
uvicorn main:app --reload
````


## Documentación de la API

* Swagger UI (Panel Interactivo): http://127.0.0.1:8000/docs
  * Aquí puedes probar los endpoints (GET, POST, PUT, DELETE) directamente.
* ReDoc (Documentación estática): http://127.0.0.1:8000/redoc



## Ejemplos de JSON (Quick Start)

Aquí tienes ejemplos de cuerpos JSON (`body`) listos para probar los endpoints en Postman.

A continuación se detallan todos los endpoints disponibles, organizados por entidad.

### Ciudades (Cities)

| Método   | Endpoint       | Descripción                                                   |
|:---------|:---------------|:--------------------------------------------------------------|
| `GET`    | `/cities/`     | Lista todas las ciudades (paginado). Params: `skip`, `limit`. |
| `GET`    | `/cities/{id}` | Obtiene una ciudad por su ID numérico.                        |
| `POST`   | `/cities/`     | Crea una nueva ciudad.                                        |
| `PUT`    | `/cities/{id}` | Actualiza datos de una ciudad existente.                      |
| `DELETE` | `/cities/{id}` | Elimina una ciudad.                                           |

#### Ejemplo de Body (POST /cities/)
**Nota:** El `Code` debe ser único y de 3 letras.

```json
{
  "Code": "PYL",
  "Name": "PythonLand",
  "Continent": "Europe",
  "Region": "Southern Europe",
  "SurfaceArea": 505990.0,
  "Population": 47000000,
  "LocalName": "República de Python",
  "GovernmentForm": "Republic",
  "Code2": "PY",
  "IndepYear": 2024,
  "LifeExpectancy": 82.5,
  "GNP": 1400000.00,
  "HeadOfState": "Guido van Rossum"
}
````
### Países (Countries)

| Método   | Endpoint            | Descripción                                                 |
|:---------|:--------------------|:------------------------------------------------------------|
| `GET`    | `/countries/`       | Lista todos los países (paginado). Params: `skip`, `limit`. |
| `GET`    | `/countries/{code}` | Obtiene un país por su código (ej: 'ESP', 'ARG').           |
| `POST`   | `/countries/`       | Crea un nuevo país. El código debe ser único.               |
| `PUT`    | `/countries/{code}` | Actualiza datos de un país.                                 |
| `DELETE` | `/countries/{code}` | Elimina un país (y sus ciudades/idiomas en cascada).        |

#### Ejemplo de Body (POST /countries/)
**Nota:** El `CountryCode` (ej: "PYL") debe existir previamente en la tabla de países.

```json
{
  "Name": "FastAPI City",
  "CountryCode": "PYL",
  "District": "Backend District",
  "Population": 150000
}
````
### Idiomas (Languages)

| Método   | Endpoint                   | Descripción                                              |
|:---------|:---------------------------|:---------------------------------------------------------|
| `GET`    | `/languages/`              | Lista todos los idiomas. Params: `skip`, `limit`.        |
| `GET`    | `/languages/{code}/{lang}` | Obtiene un idioma específico. Ej: /languages/ESP/Spanish |
| `POST`   | `/languages/`              | Asigna un idioma a un país.                              |
| `PUT`    | `/languages/{code}/{lang}` | Actualiza (ej: porcentaje o si es oficial).              |
| `DELETE` | `/languages/{code}/{lang}` | Elimina un idioma de un país.                            |

#### Ejemplo de Body (POST /languages/)
**Nota:** Esta entidad usa una clave compuesta (Código de País + Idioma).

```json
{
  "CountryCode": "PYL",
  "Language": "Pythonic",
  "IsOfficial": "T",
  "Percentage": 99.5
}
````
