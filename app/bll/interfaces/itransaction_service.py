from abc import ABC, abstractmethod

class ITransactionService(ABC):
    @abstractmethod
    def make_transfer(self, sender_id: int, receiver_id: int, amount: float) -> bool:
        pass

    @abstractmethod
    def make_payment(self, account_id: int, merchant_id: int, amount: float) -> bool:
        pass

    @abstractmethod
    def get_transaction_history(self, account_id: int) -> list:
        pass

    @abstractmethod
    def make_deposit(self, account_id: int, amount: float):
        pass

    @abstractmethod
    def get_all_transactions(self):
        pass
