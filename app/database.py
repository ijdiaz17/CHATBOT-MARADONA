from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 1. Configuración de la Base de Datos
DATABASE_URL = "sqlite:///./data/app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Modelo de la Tabla
class PredictionHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(String, index=True)
    prediction = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# 3. Función para inicializar la DB
def init_db():
    Base.metadata.create_all(bind=engine)

# 4. Función para obtener historial reciente
def get_recent_history(db, limit=3):
    """Recupera las últimas 'limit' interacciones."""
    return db.query(PredictionHistory).order_by(PredictionHistory.id.desc()).limit(limit).all()
