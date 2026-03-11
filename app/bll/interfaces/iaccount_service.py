from abc import ABC, abstractmethod

class IAccountService(ABC):
    @abstractmethod
    def open_account(self, user_id: int, account_type: str) -> int:
        pass

    @abstractmethod
    def get_account_balance(self, account_id: int) -> float:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int):
        pass

    @abstractmethod 
    def delete_account(self, account_id: int):
        pass

    @abstractmethod
    def get_all_accounts(self):
        pass
    