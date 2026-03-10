import random
from ..interfaces.iverification_service import IVerificationService
from ...dal.interfaces import IThreeDSecureRepository

class VerificationService(IVerificationService):
    def __init__(self, secure_repo: IThreeDSecureRepository):
        self.secure_repo = secure_repo

    def request_verification(self, transaction_id: int):
        code = str(random.randint(1000, 9999))
        
        verification = self.secure_repo.get_by_transaction_id(transaction_id)
        if verification:
            verification.auth_code = code
            verification.status = "PENDING"
            self.secure_repo.update(verification)
        return code

    def confirm_transaction(self, transaction_id: int, code: str) -> bool:
        verification = self.secure_repo.get_by_transaction_id(transaction_id)
        
        if verification and verification.auth_code == code:
            verification.status = "SUCCESS"
            self.secure_repo.update(verification)
            return True
        
        if verification:
            verification.status = "FAILED"
            self.secure_repo.update(verification)
        return False