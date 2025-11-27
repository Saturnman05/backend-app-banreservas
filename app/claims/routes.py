from fastapi import APIRouter, Depends

from auth.infrastructure.dependencies import get_current_user

from claims.infrastructure.repository import ClaimRepository
from claims.application.services import ClaimService

from core.database import get_db

from users.domain.models import User

router = APIRouter()


def get_claims_service(db=Depends(get_db)):
    repo = ClaimRepository(db)
    return ClaimService(repo)


@router.get("/")
async def list_claims(
    current_user: User = Depends(get_current_user),
    claim_service: ClaimService = Depends(get_claims_service),
):
    claims = claim_service.list_claims_by_user(current_user.id)
    return claims


@router.get("/account/{account_id}")
async def list_claims_by_account(
    account_id: int,
    _: User = Depends(get_current_user),
    claim_service: ClaimService = Depends(get_claims_service),
):
    claims = claim_service.list_claims_by_account(account_id)
    return claims
