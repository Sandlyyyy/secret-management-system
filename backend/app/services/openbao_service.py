import requests
import os

OPENBAO_URL = os.getenv("OPENBAO_URL", "http://openbao:5000")

class OpenBaoService:
    @staticmethod
    def get_secret(secret_name: str):
        response = requests.get(f"{OPENBAO_URL}/secrets/{secret_name}")
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def save_secret(secret_name: str, username: str, password: str, host: str = ""):
        data = {"name": secret_name, "username": username, "password": password, "host": host}
        response = requests.post(f"{OPENBAO_URL}/secrets/", json=data)
        return response.status_code == 200
