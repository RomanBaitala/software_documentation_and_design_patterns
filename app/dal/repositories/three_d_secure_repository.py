from .base_repository import BaseRepository
from ..interfaces import IThreeDSecureRepository
from ...models import ThreeDSecure

class ThreeDSecureRepository(BaseRepository[ThreeDSecure], IThreeDSecureRepository):
    def __init__(self):
        super().__init__(ThreeDSecure)

    def get_by_transaction_id(self, transaction_id: int):
        return self.model.query.filter_by(transaction_id=transaction_id).first()
    
    def update_status(self, three_d_secure_id: int, new_status: str):
        value = self.get_by_id(three_d_secure_id)
        if value:
            value.status = new_status
            self.update(value)