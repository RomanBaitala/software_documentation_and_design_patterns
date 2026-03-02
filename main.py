from app.config.ext import db
from app.app import get_app, create_app
from app.dal.repositories import UserRepository, AccountRepository, TransactionRepository
from app.dal.csv_handler import CSVDataReader
from app.bll.services.import_data_from_csv import DataImportService
from app.presentation.controller.console_conreoller import ConsoleController

app = get_app()

user_repo = UserRepository()
acc_repo = AccountRepository()
tx_repo = TransactionRepository()
csv_reader = CSVDataReader("data.csv")

import_service = DataImportService(
    user_repo=user_repo, 
    account_repo=acc_repo, 
    transaction_repo=tx_repo, 
    csv_reader=csv_reader
)

controller = ConsoleController(import_service)

if __name__ == "__main__":
    create_app()
