from claims.domain.models import Claim
from claims.infrastructure.repository import ClaimRepository
from claims.domain.exceptions import ClaimNotFound, UnauthorizedClaimAccess


class ClaimService:
    def __init__(self, repo: ClaimRepository):
        self.repo = repo

    def create_claim(self, card: Claim) -> Claim:
        return self.repo.create(card)

    def list_claims(self, account_id=None, card_id=None, user_id=None) -> list[Claim]:
        claims: list[Claim] = self.repo.list_all_filtered(
            account_id=account_id,
            card_id=card_id,
            user_id=user_id,
        )
        return claims

    def delete_claim(self, claim_id: str, user_id: int):
        claim = self.get_claim_by_id(claim_id)

        if claim.user_id != user_id:
            raise UnauthorizedClaimAccess()

        self.repo.delete(claim.id)

    def get_claim_by_id(self, claim_id: int) -> Claim:
        claim = self.repo.get_by_id(claim_id)
        if claim == None:
            raise ClaimNotFound()
