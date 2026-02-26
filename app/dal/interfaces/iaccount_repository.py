from .ibase_repository import IBaseRepository
from ...models import Account
from abc import abstractmethod

class IAccountRepository(IBaseRepository[Account]):
    @abstractmethod
    def get_all_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    def update_balance(self, account_id: int, new_balance: float):
        pass