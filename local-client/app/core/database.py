from typing import Optional, List, Dict
from .api_client import APIClient
from .database_models import User, Secret, AuditLog, SecretType, SecretStatus

class Database:
    def __init__(self, api_base_url: str = "http://192.168.0.77:8000"):
        self.api = APIClient(api_base_url)
        self._users = {}
        self._audit_logs: List[AuditLog] = []
        
        # Тестируем подключение при инициализации
        print("🔧 Testing API connection...")
        if self.api.test_connection():
            print("✅ API connection successful")
        else:
            print("❌ API connection failed - using mock mode")
    
    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация через API бэкенда"""
        print(f"🔐 Database.authenticate called for: {username}")
        
        # Пробуем API аутентификацию
        api_success = self.api.login(username, password)
        
        if api_success:
            print(f"✅ API authentication successful for: {username}")
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
            return True
        else:
            print(f"❌ API authentication failed for: {username}")
            # Fallback: временная mock аутентификация для тестирования
            if username and password:
                print(f"🔄 Using mock authentication for: {username}")
                self._users[username] = User(
                    username=username,
                    display_name=username,
                    role="user"
                )
                return True
            
            return False
    
    def get_user(self, username: str) -> Optional[User]:
        return self._users.get(username)
    
    def get_user_secrets(self, username: str) -> List[Secret]:
        """Получаем только ОДОБРЕННЫЕ секреты из API"""
        print(f"📁 Getting secrets for user: {username}")
        all_secrets = self.api.get_secrets()
        # Фильтруем только approved секреты
        approved_secrets = [s for s in all_secrets if s.status == SecretStatus.APPROVED]
        print(f"📁 Approved secrets: {len(approved_secrets)}")
        return approved_secrets
    
    def search_secrets(self, query: str, username: str) -> List[Secret]:
        """Поиск по одобренным секретам"""
        secrets = self.get_user_secrets(username)
        if not query:
            return secrets
        
        query_lower = query.lower()
        found_secrets = [
            s for s in secrets 
            if query_lower in s.name.lower() or 
               query_lower in s.description.lower() or
               any(query_lower in tag.lower() for tag in s.tags)
        ]
        print(f"🔍 Search '{query}' found {len(found_secrets)} secrets")
        return found_secrets
    
    def request_secret_access(self, secret_name: str, reason: str, username: str) -> bool:
        """Запрос доступа к секрету через веб-портал"""
        # В локальном клиенте только перенаправляем на веб-портал
        print(f"🌐 Redirecting to web portal for secret: {secret_name}")
        self.add_audit_log(
            user=username,
            action="request_access",
            resource=secret_name,
            status="redirected_to_web",
            details={"reason": reason}
        )
        return True
    
    def get_secret_value(self, secret_id: str, username: str) -> Optional[str]:
        """Получение значения секрета (только для одобренных)"""
        secrets = self.get_user_secrets(username)
        secret = next((s for s in secrets if s.id == secret_id), None)
        
        if secret and secret.status == SecretStatus.APPROVED:
            print(f"🔓 Accessing secret: {secret.name}")
            self.add_audit_log(
                user=username,
                action="access_secret",
                resource=secret.name,
                status="accessed"
            )
            return secret.value
        
        print(f"❌ Secret access denied: {secret_id}")
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