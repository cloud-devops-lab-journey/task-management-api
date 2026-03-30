from fastapi import FastAPI, HTTPException, status, Depends # --> Añadir Depends
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task

# Importar engine y Base: la conexión y la base común de SQLAlchemy
from database import engine, Base
import models       # hace que SQLAlchemy conozca la clase Task y su tabla

app = FastAPI(title="Task Management API", version="1.0.0")

# Crea en SQLite todas las tablas definidas en los modelos si no existen
Base.metadata.create_all(bind=engine)


# Modelos Pydantic
class TaskCreate(BaseModel):
    titulo: str = Field(min_length=1, description="Título de la tarea")
    contenido: str = Field(min_length=1, description="Contenido de la tarea")
    deadline: date = Field(description="Fecha de vencimiento")

class TaskUpdate(BaseModel):
    completada: bool = Field(description="Estado de completado")

class TaskResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    deadline: date
    completada: bool
    fecha_creacion: datetime

# ---------------- Nuevo codigo para TaskManager --------------
# Clase TaskManager: contiene la lógica de negocio de las tareas
class TaskManager:
    # Constructor: guarda la sesión de base de datos
    def __init__(self, db: Session):
        self._db = db

    # Método privado: limpia espacios sobrantes en texto
    def _clean_text(self, text: str) -> str:
        return text.strip()

    # Método privado: comprueba si la fecha límite ya ha pasado
    def _is_expired(self, deadline: date) -> bool:
        return deadline < date.today()

    # Crea una nueva tarea y la guarda en la base de datos
    def create_task(self, task_data: TaskCreate) -> Task:
        new_task = Task(
            titulo=self._clean_text(task_data.titulo),
            contenido=self._clean_text(task_data.contenido),
            deadline=task_data.deadline,
            completada=False
        )
        self._db.add(new_task)
        self._db.commit()
        self._db.refresh(new_task)
        return new_task

    # Busca una tarea por su id
    def get_task_by_id(self, task_id: int) -> Task:
        task = self._db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task

    # Marca una tarea como completada
    def complete_task(self, task_id: int) -> Task:
        task = self.get_task_by_id(task_id)
        task.completada = True
        self._db.commit()
        self._db.refresh(task)
        return task

    # Devuelve todas las tareas cuya fecha límite ya ha pasado
    def get_expired_tasks(self):
        return self._db.query(Task).filter(Task.deadline < date.today()).all()

    # Elimina una tarea por su id
    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        self._db.delete(task)
        self._db.commit()
# ---------------- Fin codigo para TaskManager --------------

# ----- Función auxiliar: abre una sesión de base de datos y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ----- Fin Función auxiliar:

# ----------- Endpoint: crea una nueva tarea
@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    manager = TaskManager(db)
    return manager.create_task(task)

# Endpoint: obtiene una tarea por su id
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def obtener_tarea(task_id: int, db: Session = Depends(get_db)):
    manager = TaskManager(db)
    return manager.get_task_by_id(task_id)

# Endpoint: marca una tarea como completada
@app.put("/tasks/{task_id}/completar", response_model=TaskResponse)
def marcar_completada(task_id: int, db: Session = Depends(get_db)):
    manager = TaskManager(db)
    return manager.complete_task(task_id)

# Endpoint: devuelve la lista de tareas caducadas
@app.get("/tasks/caducadas", response_model=List[TaskResponse])
def obtener_tareas_caducadas(db: Session = Depends(get_db)):
    manager = TaskManager(db)
    return manager.get_expired_tasks()

# Endpoint: elimina una tarea por su id
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(task_id: int, db: Session = Depends(get_db)):
    manager = TaskManager(db)
    manager.delete_task(task_id)
    return None

# -------------- Endpoint end --------------------

@app.get("/")
def root():
    return {"message": "Task Management API"}
