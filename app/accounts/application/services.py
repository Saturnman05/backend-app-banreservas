from accounts.infrastructure.repository import AccountRepository
from accounts.domain.models import Account


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
