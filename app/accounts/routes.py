from fastapi import APIRouter, Depends

from accounts.application.services import AccountService
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
