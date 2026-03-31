import requests
from datetime import date, timedelta

# URL base de la API en local
BASE_URL = "http://localhost:8000"


# Test: crea una tarea nueva y comprueba la respuesta
def test_crear_tarea():
    # Datos de ejemplo para crear una tarea caducada
    payload = {
        "titulo": "Tarea de prueba",
        "contenido": "Contenido de prueba",
        "deadline": str(date.today() - timedelta(days=2))
    }

    # Envía la petición POST al endpoint de creación
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)

    # Comprueba que el código HTTP sea 201
    assert response.status_code == 201, f"Error: {response.status_code} - {response.text}"

    # Convierte la respuesta a JSON
    data = response.json()

    # Comprueba algunos campos importantes de la respuesta
    assert data["titulo"] == payload["titulo"]
    assert data["contenido"] == payload["contenido"]
    assert data["deadline"] == payload["deadline"]
    assert data["completada"] is False

    # Devuelve el id creado para reutilizarlo en otros tests
    return data["id"]


# Test: obtiene una tarea por su id y comprueba la respuesta
def test_obtener_tarea(task_id):
    # Envía la petición GET al endpoint de consulta por id
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")

    # Comprueba que el código HTTP sea 200
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"

    # Convierte la respuesta a JSON
    data = response.json()

    # Comprueba que el id recibido sea el esperado
    assert data["id"] == task_id

    print(f"Test obtener tarea OK. ID obtenida: {task_id}")


# Test: marca una tarea como completada y comprueba la respuesta
def test_marcar_completada(task_id):
    # Envía la petición PUT al endpoint de completar tarea
    response = requests.put(f"{BASE_URL}/tasks/{task_id}/completar")

    # Comprueba que el código HTTP sea 200
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"

    # Convierte la respuesta a JSON
    data = response.json()

    # Comprueba que la tarea quedó marcada como completada
    assert data["id"] == task_id
    assert data["completada"] is True

    print(f"Test marcar completada OK. ID completada: {task_id}")


# Test: obtiene las tareas caducadas y comprueba que la tarea creada aparece en la lista
def test_obtener_tareas_caducadas(task_id):
    # Envía la petición GET al endpoint de tareas caducadas
    response = requests.get(f"{BASE_URL}/tasks/caducadas")

    # Comprueba que el código HTTP sea 200
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"

    # Convierte la respuesta a JSON
    data = response.json()

    # Comprueba que la respuesta sea una lista
    assert isinstance(data, list), "La respuesta no es una lista"

    # Comprueba que la tarea creada esté dentro de las tareas caducadas
    assert any(task["id"] == task_id for task in data), "La tarea no aparece en caducadas"

    print(f"Test obtener tareas caducadas OK. ID encontrada: {task_id}")


if __name__ == "__main__":
    print("Ejecutando tests...")

    # Ejecuta el test de creación
    task_id = test_crear_tarea()
    print(f"Test crear tarea OK. ID creada: {task_id}")

    # Ejecuta el test de obtención por id
    test_obtener_tarea(task_id)

    # Ejecuta el test de marcar como completada
    test_marcar_completada(task_id)

    # Ejecuta el test de tareas caducadas
    test_obtener_tareas_caducadas(task_id)

    print("Tests completados")
