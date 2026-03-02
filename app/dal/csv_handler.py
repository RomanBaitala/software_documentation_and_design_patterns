import csv
import os

class CSVDataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all(self):
        if not os.path.exists(self.file_path):
            print(f"Файл {self.file_path} не знайдено!")
            return []
        
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

from app.config.ext import db

class UserRepository:
    def add(self, user):
        db.session.add(user)

class AccountRepository:
    def add(self, account):
        db.session.add(account)

class TransactionRepository:
    def add(self, transaction):
        db.session.add(transaction)