
import requests


class APIService:
    BASE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def get(endpoint):
        try:
            response = requests.get(
                f"{APIService.BASE_URL}{endpoint}"
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error al consultar la API: {error}")
            return None

    @staticmethod
    def post(endpoint, data):
        try:
            response = requests.post(
                f"{APIService.BASE_URL}{endpoint}",
                json=data
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error al enviar datos a la API: {error}")
            return None

    @staticmethod
    def put(endpoint, data):
        try:
            response = requests.put(
                f"{APIService.BASE_URL}{endpoint}",
                json=data
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error al actualizar datos: {error}")
            return None

    @staticmethod
    def patch(endpoint, data):
        try:
            response = requests.patch(
                f"{APIService.BASE_URL}{endpoint}",
                json=data
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error al modificar datos: {error}")
            return None

    @staticmethod
    def delete(endpoint):
        try:
            response = requests.delete(
                f"{APIService.BASE_URL}{endpoint}"
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"Error al eliminar datos: {error}")
            return None
