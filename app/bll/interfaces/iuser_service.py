from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    def register_user(self, name: str, email: str, tax_id: str):
        pass

    @abstractmethod
    def get_user_profile(self, user_id: int):
        pass

    @abstractmethod
    def find_by_email(self, email: str):
        pass