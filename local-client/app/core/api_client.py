import requests
import json
from typing import Optional, List, Dict
from datetime import datetime
from .database_models import User, Secret, SecretType, SecretStatus, AuditLog

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
    
    def login(self, email: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def register(self, email: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={"email": email, "password": password}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Register error: {e}")
            return False
    
    def get_secrets(self) -> List[Secret]:
        if not self.token:
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/secrets",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                secrets_data = response.json()
                return self._convert_api_secrets(secrets_data)
            return []
        except Exception as e:
            print(f"Get secrets error: {e}")
            return []
    
    def create_secret(self, name: str, value: str) -> bool:
        if not self.token:
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/secrets",
                json={"name": name, "value": value},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Create secret error: {e}")
            return False
    
    def _convert_api_secrets(self, api_secrets: List[Dict]) -> List[Secret]:
        secrets = []
        for secret_data in api_secrets:
            secret = Secret(
                id=str(secret_data.get("id", "")),
                name=secret_data.get("name", ""),
                description="API Secret",
                type=SecretType.CUSTOM,
                status=SecretStatus.APPROVED,
                value=secret_data.get("value", ""),
                owner="current_user",
                created_at=datetime.now(),
                tags=["api"]
            )
            secrets.append(secret)
        return secrets