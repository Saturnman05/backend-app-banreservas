from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.auth.infrastructure.jwt_manager import verify_token

from app.users.domain.models import User
from app.users.infrastructure.dependencies import get_user_repository
from app.users.infrastructure.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = repo.get_by_id(user_id)
    return user
