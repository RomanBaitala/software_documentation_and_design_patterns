from .base_repository import BaseRepository
from ..interfaces import IAccountRepository
from ...models import Account

class AccountRepository(BaseRepository[Account], IAccountRepository):
    def __init__(self):
        super().__init__(Account)
    
    def get_all_by_user_id(self, user_id: int):
        return self.model.query.filter_by(user_id=user_id).all()
    
    def update_balance(self, account_id: int, new_balance: float):
        account = self.get_by_id(account_id)
        if account:
            account.balance = new_balance
            self.update(account)
    
    def get_by_card_number(self, card_number: str):
        return self.model.query.filter_by(card_number=card_number).first()