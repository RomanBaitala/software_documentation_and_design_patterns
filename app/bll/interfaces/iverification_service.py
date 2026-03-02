from abc import ABC, abstractmethod

class IVerificationService(ABC):
    @abstractmethod
    def request_verification(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def confirm_transaction(self, transaction_id: int, code: str) -> bool:
        pass
