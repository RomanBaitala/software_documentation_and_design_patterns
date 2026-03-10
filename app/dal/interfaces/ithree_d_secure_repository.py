from .ibase_repository import IBaseRepository
from ...models import ThreeDSecure
from abc import abstractmethod

class IThreeDSecureRepository(IBaseRepository[ThreeDSecure]):
    @abstractmethod
    def get_by_transaction_id(self, transaction_id: int):
        pass

    @abstractmethod
    def update_status(self, three_d_secure_id: int, new_status: str):
        pass
    