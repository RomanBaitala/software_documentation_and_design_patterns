from abc import ABC, abstractmethod

class ITransactionRepository(ABC):
    @abstractmethod
    def create_transaction(self, transaction):
        pass
    
    @abstractmethod
    def get_transaction_by_id(self, transaction_id):
        pass

    @abstractmethod
    def get_transactions_by_account_id(self, account_id):
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id):
        pass

    