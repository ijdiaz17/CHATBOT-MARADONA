# Guía de Implementación: Chatbot de Maradona

Esta guía detalla los pasos lógicos para desarrollar, desplegar y entregar el proyecto del Chatbot de Maradona accesible vía API REST.

## 1. Configuración del Entorno y Estructura del Proyecto

Antes de escribir código, organiza tu espacio de trabajo.

1.  **Crear el directorio del proyecto**:
    ```bash
    mkdir chatbot_maradona
    cd chatbot_maradona
    ```
2.  **Inicializar Git**:
    ```bash
    git init
    ```
3.  **Crear entorno virtual con Conda**:
    ```bash
    conda create --name chatbot_maradona python=3.11.9
    conda activate chatbot_maradona
    ```
4.  **Crear estructura de carpetas sugerida**:
    ```text
    CHATBOT10/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py          # Punto de entrada de la API (FastAPI/Flask)
    │   ├── model.py         # Lógica de carga y predicción del modelo LLM
    │   ├── database.py      # Lógica de conexión a la BD
    │   └── static/          # Archivos del Frontend (HTML, CSS, JS)
    ├── Dockerfile           # Configuración para Docker
    ├── requirements.txt     # Dependencias de Python
    └── README.md            # Documentación
    ```

## 2. Selección del Modelo y Base de Datos

*   **Modelo LLM**: Para desarrollo local, puedes usar un modelo pequeño de HuggingFace (ej. `distilgpt2` o un modelo de clasificación de texto) o una API externa (OpenAI) si se permite. Si los recursos son limitados, asegúrate de que el modelo corra en CPU.
*   **Base de Datos**: `sqlite3` es ideal para este alcance (local y sencillo). Se usará para guardar el historial de peticiones (prompt de entrada y respuesta del modelo).

## 3. Desarrollo del Backend (API)

Se recomienda **FastAPI** por su rapidez y documentación automática, pero Flask también es válido.

1.  **Instalar dependencias**:
    ```bash
    pip install fastapi uvicorn sqlalchemy transformers torch
    # O para Flask: pip install flask sqlalchemy transformers torch
    ```
2.  **Implementar `model.py`**:
    *   Crear una clase o función que cargue el modelo al inicio y tenga un método `predict(input_text)`.
3.  **Implementar `database.py`**:
    *   Configurar SQLAlchemy con SQLite (`sqlite:///./app.db`).
    *   Crear una tabla `PredictionHistory` con campos: `id`, `input_text`, `prediction`, `timestamp`.
4.  **Implementar `main.py`**:
    *   **Endpoint `/` (GET)**: Debe devolver instrucciones de uso (JSON o HTML renderizado).
    *   **Endpoint `/predict` (POST)**:
        *   Recibe JSON: `{"text": "..."}`
        *   Llama al modelo.
        *   Guarda la entrada y salida en la BD.
        *   Devuelve JSON: `{"prediction": "..."}`


``` fastapi dev app/main.py``` 

## 4. Desarrollo del Frontend

El frontend consumirá la API.

1.  Crear `index.html` en `app/static/`.
2.  **Diseño**: Un formulario simple con un campo de texto y un botón "Enviar".
3.  **Lógica (JS)**:
    *   Al hacer submit, usar `fetch()` para enviar un POST a `/predict`.
    *   Mostrar el resultado en pantalla.
4.  **Conexión**: Configurar FastAPI/Flask para servir archivos estáticos o crear una ruta que sirva el `index.html`.

## 5. Dockerización

1.  **Crear `requirements.txt`**:
    ```bash
    pip freeze > requirements.txt
    ```
2.  **Crear `Dockerfile`**:
    *   Base image: `python:3.11.9` (o similar).
    *   `WORKDIR /app`
    *   `COPY requirements.txt .`
    *   `RUN pip install --no-cache-dir -r requirements.txt`
    *   `COPY . .`
    *   `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]` (Ajustar comando según estructura).
3.  **Construir y probar localmente**:
    ```bash
    docker build -t chatbot-maradona .
    docker run -p 8000:80 chatbot-maradona


    docker-compose up -d

    http://localhost:8000/
    
    docker-compose down
    ```

## 6. Publicación en DockerHub

1.  Crear cuenta en [DockerHub](https://hub.docker.com/).
2.  Loguearse en terminal: `docker login`.
3.  Etiquetar la imagen:
    ```bash
    docker tag chatbot-maradona usuario_dockerhub/nombre_repositorio:tag
    ```
4.  Subir imagen:
    ```bash
    docker push usuario_dockerhub/nombre_repositorio:tag
    ```

## 7. Entregables Finales

1.  **README.md**:
    *   Título del proyecto.
    *   Descripción.
    *   Estructura de carpetas (árbol).
    *   Instrucciones de instalación local.
    *   Instrucciones para correr con Docker (comando `docker pull`).
    *   Ejemplos de uso de la API.
2.  **Repositorio**: Subir todo a GitHub (asegúrate de incluir `.gitignore` para no subir `venv` ni `__pycache__`).
