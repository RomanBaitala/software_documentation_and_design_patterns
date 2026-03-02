from ..interfaces import IAccountService
from ...dal.repositories import AccountRepository
from ...models import Account

class AccountService(IAccountService):
    def __init__(self, acc_repo: AccountRepository):
        self.acc_repo = acc_repo

    def get_total_balance(self, user_id: int) -> float:
        accounts = self.acc_repo.get_all_by_user_id(user_id)
        return sum(acc.balance for acc in accounts)

    def open_account(self, user_id: int, currency: str):
        new_account = Account(user_id=user_id, currency=currency, balance=0.0)
        return self.acc_repo.create(new_account)