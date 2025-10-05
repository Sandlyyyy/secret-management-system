from typing import Optional, List
from .database import Database, User, Secret, AuditLog, SecretType

class AuthService:
    def __init__(self, database: Database):
        self.db = database
        self.current_user: Optional[User] = None
    
    def login(self, username: str, password: str) -> bool:
        if self.db.authenticate(username, password):
            self.current_user = self.db.get_user(username)
            self.db.add_audit_log(
                user=username,
                action="login",
                resource="system",
                status="success"
            )
            return True
        return False
    
    def logout(self):
        if self.current_user:
            self.db.add_audit_log(
                user=self.current_user.username,
                action="logout", 
                resource="system",
                status="success"
            )
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        return self.current_user

class SecretService:
    def __init__(self, database: Database, auth_service: AuthService):
        self.db = database
        self.auth = auth_service
    
    def get_user_secrets(self) -> List[Secret]:
        user = self.auth.get_current_user()
        if not user:
            return []
        return self.db.get_user_secrets(user.username)
    
    def request_secret(self, name: str, description: str, secret_type: SecretType) -> bool:
        user = self.auth.get_current_user()
        if not user:
            return False
        
        return self.db.request_secret(name, description, secret_type, user.username)
    
    def get_secret_value(self, secret_id: str) -> Optional[str]:
        user = self.auth.get_current_user()
        if not user:
            return None
        
        return self.db.get_secret_value(secret_id, user.username)

class AuditService:
    def __init__(self, database: Database):
        self.db = database
    
    def get_logs(self, limit: int = 50) -> List[AuditLog]:
        return self.db.get_audit_logs(limit)
    
    def get_user_stats(self, username: str) -> dict:
        return self.db.get_user_stats(username)