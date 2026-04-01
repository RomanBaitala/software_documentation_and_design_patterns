from ..interfaces import IAccountService
from ...dal.repositories import AccountRepository
from ...models import Account, Transaction
from datetime import datetime, timezone

class AccountService(IAccountService):
    def __init__(self, acc_repo: AccountRepository):
        self.acc_repo = acc_repo

    def get_account_balance(self, user_id: int) -> float:
        accounts = self.acc_repo.get_all_by_user_id(user_id)
        return sum(acc.balance for acc in accounts)

    def open_account(self, user_id: int, card_number: int):
        new_account = Account(user_id=user_id, card_number=card_number, balance=0.0)
        return self.acc_repo.create(new_account)
    
    def get_account_by_id(self, account_id):
        account = self.acc_repo.get_by_id(account_id)

        if not account:
            raise ValueError(f"Рахунок з ID {account_id} не знайдено")
        return account
    
    def delete_account(self, account_id):
        account = self.get_account_by_id(account_id)

        if not account:
            raise ValueError(f"Рахунок з ID {account_id} не знайдено")
        
        return self.acc_repo.delete(account_id)
    
    def get_all_accounts(self):
        return self.acc_repo.get_all()
    
    
    