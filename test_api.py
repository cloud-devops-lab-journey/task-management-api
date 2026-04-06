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


# Test: envía datos incorrectos y comprueba que la API devuelve error de validación
def test_datos_incorrectos():
    # Payload incorrecto: faltan campos obligatorios y deadline no tiene formato válido
    payload = {
        "titulo": "",
        "contenido": "Contenido incorrecto",
        "deadline": "fecha-mal-formada"
    }

    # Envía la petición POST con datos inválidos
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)

    # Comprueba que la API devuelve un error de validación
    assert response.status_code in [400, 422], f"Error: {response.status_code} - {response.text}"

    print(f"Test datos incorrectos OK. Código recibido: {response.status_code}")


# Test: elimina una tarea y comprueba que después ya no existe
def test_eliminar_tarea(task_id):
    # Envía la petición DELETE al endpoint de borrado
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")

    # Comprueba que el código HTTP sea 204
    assert response.status_code == 204, f"Error: {response.status_code} - {response.text}"

    # Intenta obtener la misma tarea después de borrarla
    response_get = requests.get(f"{BASE_URL}/tasks/{task_id}")

    # Comprueba que ahora devuelve 404 porque ya no existe
    assert response_get.status_code == 404, f"Error: {response_get.status_code} - {response_get.text}"

    print(f"Test eliminar tarea OK. ID eliminada: {task_id}")


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

    # Ejecuta el test de datos incorrectos
    test_datos_incorrectos()

    # Ejecuta el test de eliminación
    test_eliminar_tarea(task_id)

    print("Tests completados")
