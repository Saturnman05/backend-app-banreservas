from app.accounts.infrastructure.repository import AccountRepository
from app.accounts.domain.models import Account
from app.accounts.domain.exceptions import (
    AccountNotFound,
    UnauthorizedAccountAccess,
)


class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo

    def create_account(self, account: Account):
        self.repo.create(account=account)
        return True

    def get_accounts_by_user(self, user_id: int):
        accounts: list[Account] = self.repo.list_all_by_user_id(user_id)
        return accounts

    def create_account(self, account: Account) -> Account:
        return self.repo.create(account)

    def get_account_by_number(self, account_number: str) -> Account:
        return self.repo.get_by_number(account_number)

    def delete_account(self, account_number: str, user_id: int):
        account = self.get_account_by_number(account_number)
        if not account:
            raise AccountNotFound()

        if account.user_id != user_id:
            raise UnauthorizedAccountAccess()
        self.repo.delete(account.id)

    def update_account(self, account_id: int, user_id: int, account_balance: float):
        account = self.repo.get_by_id(account_id)
        if not account:
            raise AccountNotFound()

        if account.user_id != user_id:
            raise UnauthorizedAccountAccess()

        return self.repo.update(account_id, balance=account_balance)
