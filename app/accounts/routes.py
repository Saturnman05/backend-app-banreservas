from fastapi import APIRouter, Depends, HTTPException

from accounts.application.dto import AccountCreate
from accounts.application.services import AccountService
from accounts.domain.models import Account
from accounts.domain.exceptions import AccountNotFound, UnauthorizedAccountAccess
from accounts.infrastructure.repository import AccountRepository

from auth.infrastructure.dependencies import get_current_user

from core.database import get_db

from users.domain.models import User

router = APIRouter()


def get_accounts_service(db=Depends(get_db)):
    repo = AccountRepository(db)
    return AccountService(repo)


@router.get("/")
async def list_accounts(
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(get_accounts_service),
):
    accounts = account_service.get_accounts_by_user(current_user.id)
    return accounts


@router.post("/")
async def create_account(
    data: AccountCreate,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(get_accounts_service),
):
    # validar que no exista cuenta con el numero de cuenta
    try:
        if account_service.get_account_by_number(data.account_number):
            raise HTTPException(400, "Ya existe una cuenta con ese número de cuenta")
    except AccountNotFound:
        pass
    except:
        raise HTTPException(500, "Server error")

    account = Account(
        id=None,
        user_id=current_user.id,
        account_number=data.account_number,
        account_type=data.account_type,
        balance=data.balance,
    )

    account = account_service.create_account(account)

    return {
        "message": "Usuario creado exitosamente",
        "account": {
            "id": account.id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": account.balance,
        },
    }


@router.delete("/{account_number}")
async def delete_account(
    account_number: str,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(get_accounts_service),
):
    try:
        account_service.delete_account(account_number, current_user.id)
    except AccountNotFound:
        raise HTTPException(
            status_code=404, detail=f"La cuenta {account_number} no existe"
        )
    except UnauthorizedAccountAccess:
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar esta cuenta"
        )

    return {"message": f"La cuenta {account_number} se elimino exitosamente"}
