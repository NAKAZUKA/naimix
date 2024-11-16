from passlib.context import CryptContext

# Настройка для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли предоставленный пароль хэшированному.
    """
    return pwd_context.verify(plain_password, hashed_password)
