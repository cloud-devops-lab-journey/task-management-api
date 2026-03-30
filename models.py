from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from datetime import datetime
from database import Base

# Clase Task: representa la tabla de tareas en la base de datos
class Task(Base):
    # Nombre de la tabla en SQLite
    __tablename__ = "tasks"

    # Clave primaria única de cada tarea
    id = Column(Integer, primary_key=True, index=True)

    # Título de la tarea (obligatorio)
    titulo = Column(String, nullable=False)

    # Contenido o descripción de la tarea (obligatorio)
    contenido = Column(String, nullable=False)

    # Fecha límite de la tarea
    deadline = Column(Date, nullable=False)

    # Indica si la tarea está completada
    completada = Column(Boolean, default=False)

    # Fecha y hora de creación de la tarea
    fecha_creacion = Column(DateTime, default=datetime.utcnow)