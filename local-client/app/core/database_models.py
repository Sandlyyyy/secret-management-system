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