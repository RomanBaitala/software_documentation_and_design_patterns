from ..interfaces.iuser_service import IUserService
from ...dal.interfaces import IUserRepository
from ...models import User

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def register_user(self, name: str, email: str, tax_id: str):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            return existing_user

        if self.user_repo.get_by_tax_id(tax_id):
            raise ValueError(f"Користувач з податковим номером {tax_id} вже існує")

        new_user = User(
            name=name,
            email=email,
            tax_id=tax_id
        )

        return self.user_repo.create(new_user)

    def get_user_profile(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        return user

    def find_by_email(self, email: str):
        return self.user_repo.get_by_email(email)