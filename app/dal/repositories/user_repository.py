from .base_repository import BaseRepository
from ..interfaces import IUserRepository
from ...models import User

class UserRepository(BaseRepository[User], IUserRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str):
        return self.model.query.filter_by(email=email).first()
    
    def get_by_tax_id(self, tax_id: str):
        return self.model.query.filter_by(tax_id=tax_id).first()