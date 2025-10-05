import requests
import os

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM = "master"
CLIENT_ID = "secret-client"

class AuthService:
    @staticmethod
    def validate_token(token: str):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
