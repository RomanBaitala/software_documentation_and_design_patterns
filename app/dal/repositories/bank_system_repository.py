from .base_repository import BaseRepository
from ..interfaces import IBankSystemRepository
from ...models import BankSystem

class BankSystemRepository(BaseRepository[BankSystem], IBankSystemRepository):
    def __init__(self):
        super().__init__(BankSystem)

    def get_by_mfo(self, mfo: str):
        return self.model.query.filter_by(mfo=mfo).first()

