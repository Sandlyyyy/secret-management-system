import requests
import json
from typing import Optional, List, Dict
from datetime import datetime
from .database_models import User, Secret, SecretType, SecretStatus, AuditLog

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
        print(f"APIClient initialized with URL: {base_url}")
    
    def test_connection(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            print(f"Connection test: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        print(f"API Login attempt: {email}")
        
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"email": email, "password": password},
                timeout=10
            )
            
            print(f"API Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                print(f"API Login successful")
                return True
            else:
                print(f"API Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"API Login error: {e}")
            return False
    
    def register(self, email: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json={"email": email, "password": password},
                timeout=10
            )
            print(f"Register response: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Register error: {e}")
            return False
    
    def get_secrets(self) -> List[Secret]:
        if not self.token:
            print("No token for get_secrets")
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/secrets",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=10
            )
            
            print(f"Get secrets response: {response.status_code}")
            
            if response.status_code == 200:
                secrets_data = response.json()
                print(f"Found {len(secrets_data)} secrets")
                return self._convert_api_secrets(secrets_data)
            else:
                print(f"Get secrets failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Get secrets error: {e}")
            return []
    
    def get_all_secrets(self) -> List[Secret]:
        return self.get_secrets()
    
    def create_secret(self, name: str, value: str) -> bool:
        if not self.token:
            print("No token for create_secret")
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/secrets",
                json={"name": name, "value": value},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=10
            )
            
            print(f"Create secret response: {response.status_code}")
            return response.status_code == 200
            
        except Exception as e:
            print(f"Create secret error: {e}")
            return False
    
    def _convert_api_secrets(self, api_secrets: List[Dict]) -> List[Secret]:
        secrets = []
        
        if not api_secrets:
            print("No secrets data from API")
            return secrets
            
        for i, secret_data in enumerate(api_secrets):
            try:
                secret = Secret(
                    id=str(secret_data.get("id", i)),
                    name=secret_data.get("name", f"Secret {i}"),
                    description=secret_data.get("description", "API Secret"),
                    type=SecretType.CUSTOM,
                    status=SecretStatus.APPROVED,
                    value=secret_data.get("value", ""),
                    owner=secret_data.get("owner", "current_user"),
                    created_at=datetime.now(),
                    tags=["api"]
                )
                secrets.append(secret)
            except Exception as e:
                print(f"Error converting secret {i}: {e}")
        
        print(f"Converted {len(secrets)} secrets from API")
        return secrets