# Chatbot Maradona 🔟

Este proyecto implementa un chatbot basado en LLM que imita la personalidad de Diego Armando Maradona. Utiliza **RAG (Retrieval-Augmented Generation)** para responder con frases icónicas y contexto relevante almacenado en una base de datos vectorial.

<img src="docs/screenshoot/conversacion_diego.gif" width="300" alt="Demo" />

## 🚀 Características

- **Backend**: FastAPI para una API rápida y moderna.
- **IA**: Integración con OpenAI y ChromaDB para búsqueda semántica.
- **Persistencia**:
    - `app.db` (SQLite): Historial de conversaciones.
    - `chroma_db/`: Base de datos vectorial con el conocimiento del bot.
- **Docker**: Contenedorizado y listo para desplegar.

## 📂 Estructura del Proyecto

```text
CHATBOT10/
├── app/                 # Código fuente
│   ├── main.py          # API FastAPI y lógica principal
│   ├── database.py      # Modelos de base de datos
│   ├── model.py         # Lógica RAG y OpenAI
│   └── static/          # Frontend (HTML, CSS, Imágenes)
├── data/                # Datos persistentes
│   ├── app.db           # Base de datos SQLite (Historial)
│   ├── chroma_db/       # Base de datos vectorial
│   └── raw/             # Archivos de texto originales
├── docs/                # Documentación
├── notebooks/           # Jupyter Notebooks
├── Dockerfile           # Configuración de imagen Docker
├── docker-compose.yml   # Orquestación de contenedores
├── requirements.txt     # Dependencias de Python
└── README.md            # Documentación
```

## 🛠️ Instalación Local

1.  **Clonar el repositorio**:
    ```bash
    git clone <tu-repo-url>
    cd CHATBOT10
    ```

2.  **Crear entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno**:
    Crea un archivo `.env` en la raíz con tu API Key de OpenAI:
    ```env
    OPENAI_API_KEY=...
    ```

5.  **Ejecutar la aplicación**:
    ```bash
    fastapi dev app/main.py
    ```
    Accede a `http://localhost:8000`.

## 🐳 Uso con Docker

### Opción A: Descargar desde Docker Hub (Recomendado)

Esta imagen **ya incluye la personalidad y memoria de Diego** (base de datos vectorial y app.db). Puedes descargarla y ejecutarla directamente:

```bash
docker pull ijdiaz17/chatbot10:latest
```

Para ejecutarla:
```bash
docker run -p 8000:8000 --env-file .env ijdiaz17/chatbot10:latest
```
*Nota: Al reiniciar el contenedor, el historial de **nuevas** conversaciones se perderá, pero la personalidad de Diego se mantendrá intacta.*

### Opción B: Docker Compose

Si tienes el código fuente, puedes usar Docker Compose para gestionar la configuración fácilmente:

```bash
docker-compose up -d
```

2. Accede a: `http://localhost:8000`.

3. Para detenerlo:
```bash
docker-compose down
```

## 🔌 Uso de la API

La API cuenta con documentación automática en `/docs`.

-   **Interfaz Web**: `GET /` -> Carga el chat visual.
-   **Chat**: `POST /chat`
    -   Body: `{"message": "¿Quién eres?"}`
    -   Response: `{"response": "Soy el Diego, pibe..."}`

---
Desarrollado con 💙 y ⚽.
