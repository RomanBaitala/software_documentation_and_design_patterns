from .ibase_repository import IBaseRepository
from ...models import BankSystem
from abc import abstractmethod

class IBankSystemRepository(IBaseRepository[BankSystem]):
    @abstractmethod
    def get_by_mfo(self, mfo: str):
        pass