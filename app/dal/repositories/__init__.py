from .account_repository import AccountRepository
from .transaction_repository import TransactionRepository
from .user_repository import UserRepository
from .three_d_secure_repository import ThreeDSecureRepository
from .bank_system_repository import BankSystemRepository

account_repository = AccountRepository()
transaction_repository = TransactionRepository()
user_repository = UserRepository()
bank_system_repository = BankSystemRepository()
three_d_secure_repository = ThreeDSecureRepository()
