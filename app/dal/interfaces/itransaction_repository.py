from .ibase_repository import IBaseRepository
from ...models import Transaction
from abc import abstractmethod

class ITransactionRepository(IBaseRepository[Transaction]):
    @abstractmethod
    def get_by_account_id(self, account_id):
        pass

    @abstractmethod
    def get_by_receiver_account_id(self, account_id):
        pass

    @abstractmethod
    def get_by_transaction_type(self, transaction_type):
        pass

    @abstractmethod
    def get_all_with_first_date(self):
        pass


    