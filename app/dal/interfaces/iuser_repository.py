from .ibase_repository import IBaseRepository
from ...models import User
from abc import abstractmethod

class IUserRepository(IBaseRepository[User]):
    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def get_by_tax_id(self, tax_id: str):
        pass