from .base_repository import BaseRepository
from ..interfaces import ITransactionRepository
from ...models import Transaction

class TransactionRepository(BaseRepository[Transaction], ITransactionRepository):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_account_id(self, account_id):
        return self.model.query.filter_by(account_id=account_id).all()
    
    def get_by_receiver_account_id(self, account_id):
        return self.model.query.filter_by(receiver_account_id=account_id).all()
    
    def get_by_transaction_type(self, transaction_type):
        return self.model.query.filter_by(transaction_type=transaction_type).all()
    
    def get_all_with_first_date(self):
        return self.model.query.order_by(self.model.timestamp.desc()).all()