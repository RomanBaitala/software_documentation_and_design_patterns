from abc import ABC, abstractmethod

class IAccountService(ABC):
    @abstractmethod
    def open_account(self, user_id: int, account_type: str) -> int:
        pass

    @abstractmethod
    def block_card(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def get_account_balance(self, account_id: int) -> float:
        pass