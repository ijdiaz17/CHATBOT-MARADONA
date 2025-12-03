from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, PredictionHistory, init_db, get_recent_history
from app.model import generar_respuesta

# Inicializamos la base de datos (crea las tablas si no existen)
init_db()

# Creamos la instancia de la aplicación FastAPI
app = FastAPI()

# Montar carpeta static para archivos CSS, JS e imágenes
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- Modelos de Datos (Pydantic) ---
# Definimos la estructura de los datos que esperamos recibir.
# Esto ayuda a FastAPI a validar los datos automáticamente.
class Consulta(BaseModel):
    mensaje: str

# --- Dependencias ---
# Función para obtener una sesión de base de datos.
# Se usa con `Depends` para asegurar que cada petición tenga su propia sesión
# y que se cierre correctamente al terminar.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints (Rutas) ---

@app.get("/")
def root():
    """
    Ruta raíz. Sirve el archivo index.html del frontend.
    """
    return FileResponse('app/static/index.html')

@app.post("/chat")
def chat(consulta: Consulta, db: Session = Depends(get_db)):
    """
    Endpoint principal para hablar con el Diego.
    
    Argumentos:
    - consulta: Un objeto JSON con el campo 'mensaje' (validado por Pydantic).
    - db: La sesión de base de datos inyectada por FastAPI.
    
    Retorna:
    - Un JSON con la respuesta generada.
    """
    # 1. Obtener historial reciente para contexto
    historial = get_recent_history(db)

    # 2. Generar respuesta usando la lógica del modelo (app/model.py)
    respuesta_texto = generar_respuesta(consulta.mensaje, historial)
    
    # 3. Guardar la interacción en la base de datos (app/database.py)
    # Creamos una nueva instancia del modelo PredictionHistory
    nueva_prediccion = PredictionHistory(
        input_text=consulta.mensaje,
        prediction=respuesta_texto
    )
    
    # Añadimos y confirmamos los cambios en la DB
    db.add(nueva_prediccion)
    db.commit()
    # Refrescamos el objeto para obtener datos generados por la DB (como el ID o timestamp)
    db.refresh(nueva_prediccion)
    
    return {"respuesta": respuesta_texto}
