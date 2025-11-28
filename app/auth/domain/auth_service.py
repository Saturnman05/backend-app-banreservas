from passlib.context import CryptContext
from users.infrastructure.repository import UserRepository
from auth.domain.exceptions import InvalidCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str):
        user = self.repo.get_by_username(username)

        if not user:
            raise InvalidCredentials("Usuario no existe")

        if not pwd_context.verify(password, user.hashed_password):
            raise InvalidCredentials("Contraseña incorrecta")

        return user

    @staticmethod
    def hash_password(password: str) -> str:
        password = password[:72]
        return pwd_context.hash(password)
