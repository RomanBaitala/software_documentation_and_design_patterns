from ..interfaces.iuser_service import IUserService
from ...dal.interfaces import IUserRepository
from ...models import User


class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo


    def register_user(self, name: str, email: str, tax_id: str, password: str, surname: str):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            return existing_user

        if self.user_repo.get_by_tax_id(tax_id):
            raise ValueError(f"Користувач з податковим номером {tax_id} вже існує")

        new_user = User(
            name=name,
            email=email,
            password=password,
            surname=surname,
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
    

    def get_all_users(self):
        return self.user_repo.get_all()
    

    def update_user(self, user_id: int, data: dict):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Користувача з ID {user_id} не знайдено")

        new_email = data.get('email')
        if new_email and new_email != user.email:
            if self.user_repo.get_by_email(new_email):
                raise ValueError(f"Email {new_email} вже зайнятий")

        user.name = data.get('name', user.name)
        user.surname = data.get('surname', user.surname)
        user.email = data.get('email', user.email)
        user.tax_id = data.get('tax_id', user.tax_id)

        return self.user_repo.update(user)


    def delete_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Користувача не знайдено, видалення неможливе.")
        
        return self.user_repo.delete(user_id)