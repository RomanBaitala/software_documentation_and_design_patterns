import os
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from dotenv import load_dotenv

from app.config.ext import db
# Імпорт маршрутів (контролерів)
# from app.presentation.routes.admin_routes import admin_bp
from app.presentation.routes.user_routes import user_bp

load_dotenv()

def init_mysql_database(db_url):
    """Створює схему в MySQL, якщо її немає"""
    url = make_url(db_url)
    
    base_url = f"mysql+pymysql://{url.username}:{url.password}@{url.host}:{url.port or 3306}"
    engine = create_engine(base_url)
    
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {url.database}"))
        conn.commit() 
        
    print(f"База даних '{url.database}' готова.")

def create_app():
    app = Flask(__name__, 
                template_folder='app/presentation/templates', 
                static_folder='app/presentation/static')
    
    db_url = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_mysql_database(db_url)

    db.init_app(app)

    # app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()
        print("Таблиці бази даних синхронізовано.")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)