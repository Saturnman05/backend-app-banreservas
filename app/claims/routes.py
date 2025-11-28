from fastapi import APIRouter, Depends

from auth.infrastructure.dependencies import get_current_user

from claims.domain.models import Claim
from claims.infrastructure.repository import ClaimRepository
from claims.application.services import ClaimService
from claims.application.dto import ClaimCreateDto

from core.database import get_db

from users.domain.models import User

router = APIRouter()


def get_claims_service(db=Depends(get_db)):
    repo = ClaimRepository(db)
    return ClaimService(repo)


@router.get("/")
async def list_claims(
    account_id: int | None = None,
    card_id: int | None = None,
    current_user: User = Depends(get_current_user),
    claim_service: ClaimService = Depends(get_claims_service),
):
    # claims = claim_service.list_claims_by_user(current_user.id)
    claims = claim_service.list_claims(
        account_id=account_id,
        user_id=current_user.id,
        card_id=card_id,
    )
    return claims


@router.post("/")
async def create_claim(
    data: ClaimCreateDto,
    current_user: User = Depends(get_current_user),
    claim_service: ClaimService = Depends(get_claims_service),
):
    claim = Claim(
        id=None,
        user_id=current_user.id,
        account_id=data.account_id,
        card_id=data.card_id,
        claim_description=data.claim_description,
        claim_type=data.claim_type,
    )

    claim = claim_service.create_claim(claim)

    return {
        "message": "Reclamacion creada exitosamente",
        "claim": {
            "id": claim.id,
            "claim_description": claim.claim_description,
            "claim_type": claim.claim_type,
        },
    }
