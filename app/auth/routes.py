from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth.application.dto import UserRegisterDTO
from auth.domain.auth_service import AuthService
from auth.domain.exceptions import InvalidCredentials
from auth.infrastructure.jwt_manager import create_access_token

from users.domain.models import User
from users.domain.exceptions import UserNotFound
from users.infrastructure.dependencies import get_user_repository
from users.infrastructure.repository import UserRepository


router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repository),
):
    auth_service = AuthService(repo)

    try:
        user = auth_service.authenticate(form_data.username, form_data.password)
    except InvalidCredentials as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(
    data: UserRegisterDTO, repo: UserRepository = Depends(get_user_repository)
):

    # Validar que el usuario no exista
    try:
        if repo.get_by_username(data.username):
            raise HTTPException(400, "El nombre de usuario ya existe")
    except UserNotFound:
        pass

    try:
        if repo.get_by_email(data.email):
            raise HTTPException(400, "El correo ya está en uso")
    except UserNotFound:
        pass

    # Hashear contraseña
    hashed = AuthService.hash_password(data.password)

    # Crear entidad del dominio
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        username=data.username,
        hashed_password=hashed,
    )

    # Guardar en BD
    created_user = repo.create(user)

    # Crear token de acceso automáticamente
    token = create_access_token({"sub": created_user.id})

    return {
        "message": "Usuario creado exitosamente",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": created_user.id,
            "username": created_user.username,
            "email": created_user.email,
            "full_name": created_user.full_name(),
        },
    }
