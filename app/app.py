import os
import mysql.connector
from flask import Flask
from sqlalchemy.engine import make_url
from dotenv import load_dotenv
from .config.ext import db

from app.dal.repositories import UserRepository, AccountRepository, TransactionRepository
from app.dal.csv_handler import CSVDataReader
from app.bll.services.import_data_from_csv import DataImportService

load_dotenv()
app = Flask(__name__)


def init_mysql_database(db_url):
    """Створює саму схему в MySQL через сирий конектор"""
    url = make_url(db_url)
    connection = mysql.connector.connect(
        host=url.host,
        user=url.username,
        password=url.password,
        port=url.port or 3306
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {url.database}")
    cursor.close()
    connection.close()
    print(f"База даних '{url.database}' готова.")

def create_app():
    db_url = os.getenv("DATABASE_URL")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_mysql_database(db_url)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        user_repo = UserRepository()
        acc_repo = AccountRepository()
        tx_repo = TransactionRepository()
        csv_reader = CSVDataReader("data.csv")

        service = DataImportService(user_repo, acc_repo, tx_repo, csv_reader)
        
        service.import_all_data()

    return app

def get_app():
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
