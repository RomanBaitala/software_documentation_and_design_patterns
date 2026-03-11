from datetime import datetime, timezone
from ..interfaces.itransaction_service import ITransactionService
from ...dal.interfaces import ITransactionRepository, IAccountRepository
from ...models import Transfer, Payment, Transaction

class TransactionService(ITransactionService):
    def __init__(self, tx_repo: ITransactionRepository, acc_repo: IAccountRepository):
        self.tx_repo = tx_repo
        self.acc_repo = acc_repo

    def make_transfer(self, sender_id: int, receiver_id: int, amount: float):
        if amount <= 0:
            raise ValueError("Сума має бути більшою за нуль")

        sender = self.acc_repo.get_by_id(sender_id)
        receiver = self.acc_repo.get_by_id(receiver_id)

        if not sender or not receiver:
            raise ValueError("Рахунок не знайдено")

        if sender.balance < amount:
            raise ValueError("Недостатньо коштів на рахунку відправника")

        sender.balance -= amount
        receiver.balance += amount

        self.acc_repo.update(sender)
        self.acc_repo.update(receiver)

        debit_tx = Transfer(
            sender_account_id=sender_id,
            receiver_account_id=receiver_id,
            amount=amount,
            type='transfer',
            category="Списання коштів" 
        )
        self.tx_repo.create(debit_tx)

        credit_tx = Transfer(
            sender_account_id=sender_id,
            receiver_account_id=receiver_id,
            amount=amount,
            type='transfer',
            category="Зарахування коштів"
        )
        self.tx_repo.create(credit_tx)

        return debit_tx

    def make_payment(self, sender_id: int, merchant_id: int, amount: float, merchant_name: str):
        sender = self.acc_repo.get_by_id(sender_id)
        
        if sender.balance < amount:
            raise ValueError("Недостатньо коштів для оплати")

        sender.balance -= amount
        self.acc_repo.update(sender)

        new_payment = Payment(
            sender_account_id=sender_id,
            receiver_account_id=merchant_id,
            amount=amount,
            merchant_name=merchant_name,
            timestamp=datetime.now(timezone.utc)
        )
        return self.tx_repo.create(new_payment)
    
    def get_transaction_history(self, account_id: int):
        return self.tx_repo.get_by_account_id(account_id)
    
    def make_deposit(self, account_id: int, amount: float):
        if amount <= 0:
            raise ValueError("Сума поповнення має бути більшою за нуль")

        account = self.acc_repo.get_by_id(account_id)
        if not account:
            raise ValueError("Рахунок не знайдено")

        account.balance += amount
        self.acc_repo.update(account)

        deposit_tx = Transaction(
            sender_account_id=account_id,
            receiver_account_id=account_id,
            amount=amount,
            type='deposit',
            timestamp=datetime.now(timezone.utc)
        )
        return self.tx_repo.create(deposit_tx)