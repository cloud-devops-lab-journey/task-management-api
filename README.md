# Task Management API

API REST para la gestión de tareas desarrollada con FastAPI.

## Instalación

### 1. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Puedes usar cualquiera de estos comandos:

```bash
# Opción 1: Comando moderno de FastAPI (recomendado)
fastapi dev main.py

# Opción 2: Uvicorn tradicional
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Endpoints

- `GET /` - Mensaje de bienvenida de la API
- `POST /tasks/` - Crear una nueva tarea
- `GET /tasks/caducadas` - Obtener la lista de tareas caducadas
- `GET /tasks/{task_id}` - Obtener una tarea por ID
- `PUT /tasks/{task_id}/completar` - Marcar una tarea como completada
- `DELETE /tasks/{task_id}` - Eliminar una tarea por ID

## Funcionalidades

La API permite:

- Crear tareas con título, contenido y fecha límite
- Consultar una tarea a partir de su ID
- Marcar una tarea como completada
- Obtener la lista de tareas caducadas
- Eliminar tareas
- Guardar la información en una base de datos SQLite
- Probar automáticamente los endpoints con un script en Python usando `requests`

## Ejecutar tests

```bash
python test_api.py
```

## Documentación interactiva

Una vez ejecutando la aplicación, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
