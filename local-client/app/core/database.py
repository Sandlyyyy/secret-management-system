from typing import Optional, List, Dict
from .api_client import APIClient
from .database_models import User, Secret, AuditLog, SecretType, SecretStatus

class Database:
    def __init__(self, api_base_url: str = "http://192.168.0.77:8000"):  # ТВОЙ IP!
        self.api = APIClient(api_base_url)
        self._users = {}
        self._audit_logs: List[AuditLog] = []
    
    def authenticate(self, username: str, password: str) -> bool:
        success = self.api.login(username, password)
        if success:
            self._users[username] = User(
                username=username,
                display_name=username,
                role="user"
            )
            self.add_audit_log(
                user=username,
                action="login",
                resource="system",
                status="success"
            )
        else:
            self.add_audit_log(
                user=username,
                action="login",
                resource="system",
                status="failed"
            )
        return success
    
    def get_user(self, username: str) -> Optional[User]:
        return self._users.get(username)
    
    def get_user_secrets(self, username: str) -> List[Secret]:
        return self.api.get_secrets()
    
    def request_secret(self, name: str, description: str, secret_type: SecretType, username: str) -> bool:
        success = self.api.create_secret(name, description)
        if success:
            self.add_audit_log(
                user=username,
                action="request_secret",
                resource=name,
                status="success"
            )
        return success
    
    def get_secret_value(self, secret_id: str, username: str) -> Optional[str]:
        secrets = self.api.get_secrets()
        secret = next((s for s in secrets if s.id == secret_id), None)
        if secret:
            self.add_audit_log(
                user=username,
                action="access_secret",
                resource=secret.name,
                status="accessed"
            )
            return secret.value
        return None
    
    def add_audit_log(self, user: str, action: str, resource: str, status: str, details: Dict = None):
        from datetime import datetime
        log = AuditLog(
            timestamp=datetime.now(),
            user=user,
            action=action,
            resource=resource,
            status=status,
            details=details
        )
        self._audit_logs.append(log)
    
    def get_audit_logs(self, limit: int = 50) -> List[AuditLog]:
        return self._audit_logs[-limit:]
    
    def get_user_stats(self, username: str) -> Dict[str, int]:
        secrets = self.get_user_secrets(username)
        return {
            "total": len(secrets),
            "approved": len(secrets),
            "pending": 0,
            "rejected": 0
        }