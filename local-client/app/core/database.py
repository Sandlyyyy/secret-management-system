from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum

class SecretType(Enum):
    DATABASE = "database"
    API = "api" 
    CLOUD = "cloud"
    SECURITY = "security"
    EMAIL = "email"
    CUSTOM = "custom"

class SecretStatus(Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"

@dataclass
class User:
    username: str
    display_name: str
    role: str

@dataclass
class Secret:
    id: str
    name: str
    description: str
    type: SecretType
    status: SecretStatus
    value: str
    owner: str
    created_at: datetime
    approved_by: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class AuditLog:
    timestamp: datetime
    user: str
    action: str
    resource: str
    status: str
    details: Optional[Dict] = None

class Database:
    def __init__(self):
        self._users = self._create_users()
        self._secrets = self._create_secrets()
        self._audit_logs: List[AuditLog] = []
    
    def _create_users(self) -> Dict[str, User]:
        return {
            "admin": User("admin", "👑 Администратор", "admin"),
            "demo": User("demo", "👤 Демо-пользователь", "user"),
            "user": User("user", "👥 Обычный пользователь", "user"),
            "test": User("test", "🧪 Тестовый пользователь", "user")
        }
    
    def _create_secrets(self) -> List[Secret]:
        now = datetime.now()
        return [
            Secret(
                id="1",
                name="Production Database",
                description="Основные учетные данные PostgreSQL для продакшена",
                type=SecretType.DATABASE,
                status=SecretStatus.APPROVED,
                value="postgresql://admin:ProdDB2024!@db-prod.company.com:5432/production",
                owner="admin",
                created_at=now - timedelta(days=5),
                approved_by="system",
                tags=["database", "production", "critical"]
            ),
            Secret(
                id="2", 
                name="Stripe Live API",
                description="API ключ для обработки платежей в продакшене",
                type=SecretType.API,
                status=SecretStatus.APPROVED,
                value="sk_live_51Mn789LkjhgFDS456QWErty1234abc789",
                owner="demo", 
                created_at=now - timedelta(days=3),
                approved_by="admin",
                tags=["payment", "api", "production"]
            ),
            Secret(
                id="3",
                name="AWS S3 Bucket",
                description="Учетные данные для облачного хранилища пользовательских файлов",
                type=SecretType.CLOUD, 
                status=SecretStatus.PENDING,
                value="",
                owner="user",
                created_at=now - timedelta(days=1),
                tags=["aws", "storage", "cloud"]
            ),
            Secret(
                id="4",
                name="JWT Secret Key", 
                description="Секретный ключ для аутентификации приложения",
                type=SecretType.SECURITY,
                status=SecretStatus.APPROVED,
                value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.supersecret.key123456789",
                owner="admin",
                created_at=now,
                approved_by="system", 
                tags=["authentication", "jwt", "security"]
            )
        ]
    
    def authenticate(self, username: str, password: str) -> bool:
        passwords = {
            "admin": "admin123",
            "demo": "demo123", 
            "user": "user123",
            "test": "test123"
        }
        return passwords.get(username) == password
    
    def get_user(self, username: str) -> Optional[User]:
        return self._users.get(username)
    
    def get_user_secrets(self, username: str) -> List[Secret]:
        user = self.get_user(username)
        if not user:
            return []
        
        if user.role == "admin":
            return self._secrets.copy()
        else:
            return [s for s in self._secrets if s.owner == username or s.status == SecretStatus.APPROVED]
    
    def request_secret(self, name: str, description: str, secret_type: SecretType, username: str) -> bool:
        new_secret = Secret(
            id=str(len(self._secrets) + 1),
            name=name,
            description=description, 
            type=secret_type,
            status=SecretStatus.PENDING,
            value="",
            owner=username,
            created_at=datetime.now(),
            tags=[secret_type.value]
        )
        self._secrets.append(new_secret)
        
        self.add_audit_log(
            user=username,
            action="request_secret",
            resource=name,
            status="pending"
        )
        return True
    
    def get_secret_value(self, secret_id: str, username: str) -> Optional[str]:
        secret = next((s for s in self._secrets if s.id == secret_id), None)
        if not secret:
            return None
        
        if secret.status != SecretStatus.APPROVED:
            return None
        
        self.add_audit_log(
            user=username,
            action="access_secret", 
            resource=secret.name,
            status="accessed"
        )
        return secret.value
    
    def add_audit_log(self, user: str, action: str, resource: str, status: str, details: Dict = None):
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
        return sorted(self._audit_logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_user_stats(self, username: str) -> Dict[str, int]:
        secrets = self.get_user_secrets(username)
        return {
            "total": len(secrets),
            "approved": len([s for s in secrets if s.status == SecretStatus.APPROVED]),
            "pending": len([s for s in secrets if s.status == SecretStatus.PENDING]),
            "rejected": len([s for s in secrets if s.status == SecretStatus.REJECTED])
        }