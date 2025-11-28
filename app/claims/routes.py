from fastapi import APIRouter, Depends, HTTPException

from auth.infrastructure.dependencies import get_current_user

from claims.domain.models import Claim
from claims.infrastructure.repository import ClaimRepository
from claims.application.services import ClaimService
from claims.application.dto import ClaimCreateDto
from claims.domain.exceptions import ClaimNotFound, UnauthorizedClaimAccess

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


@router.delete("/{claim_id}")
async def delete_claim(
    claim_id: int,
    current_user: User = Depends(get_current_user),
    claim_service: ClaimService = Depends(get_claims_service),
):
    try:
        claim_service.delete_claim(claim_id, current_user.id)
    except ClaimNotFound:
        raise HTTPException(
            status_code=404, detail=f"La reclamacion {claim_id} no existe"
        )
    except UnauthorizedClaimAccess:
        raise HTTPException(
            status_code=403, detail="No tienes permiso para eliminar esta reclamacion"
        )

    return {"message": f"La reclamacion {claim_id} se elimino exitosamente"}
