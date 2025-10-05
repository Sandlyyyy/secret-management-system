from cryptography.fernet import Fernet

def generate_key(master_password: str):
    return Fernet(master_password.encode("utf-8").ljust(32)[:32])

def encrypt(data: str, key: bytes):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt(token: str, key: bytes):
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()
