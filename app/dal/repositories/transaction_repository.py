from ..interfaces.itransaction_repository import ITransactionRepository
from ...models.transaction import Transaction
from ...config.ext import db

class TransactionRepository(ITransactionRepository):
    def create_transaction(self, transaction):
        db.session.add(transaction)
        db.session.commit()
        return transaction
    
    def get_transaction_by_id(self, transaction_id):
        return Transaction.query.get(transaction_id)

    def get_transactions_by_account_id(self, account_id):
        return Transaction.query.filter(
            (Transaction.sender_account_id == account_id) | 
            (Transaction.receiver_account_id == account_id)
        ).all()
    