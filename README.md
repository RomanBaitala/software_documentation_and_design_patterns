## Software documentation

# Finance Data Management System

Проєкт для автоматизації генерації, обробки та імпорту банківських даних (користувачі, рахунки, транзакції) з використанням багатошарової архітектури та ORM SQLAlchemy.

## Технології

* **Мова:** Python 3.10+
* **Framework:** Flask (керування контекстом та конфігурацією)
* **ORM:** SQLAlchemy (Flask-SQLAlchemy)
* **База даних:** MySQL 8.0+ (драйвер PyMySQL)
* **Формат даних:** CSV
* **Конфігурація:** python-dotenv (керування `.env` файлами)

---

## Архітектура проєкту

Проєкт реалізований за принципом **Layered Architecture (Багатошарова архітектура)**. Це забезпечує незалежність бізнес-логіки від бази даних та інтерфейсу.

### Структура шарів:

1.  **DAL (Data Access Layer) — Рівень доступу до даних**
    * `repositories/`: Інкапсулюють логіку запитів до БД (UserRepository, AccountRepository тощо).
    * `csv_handler.py`: Відповідає за читання сирих даних з файлової системи.
2.  **BLL (Business Logic Layer) — Рівень бізнес-логіки**
    * `services/`: Головний сервіс `DataImportService` координує процес: перевіряє унікальність об'єктів, створює зв'язки (Relationships) та керує транзакціями БД.
3.  **Models Layer — Моделі даних**
    * Використовується **Joined Table Inheritance** (спадкування таблиць) для сутностей `Transaction`, `Payment` та `Transfer`.
4.  **Presentation Layer — Рівень представлення**
    * `ConsoleController`: Консольний інтерфейс для взаємодії з користувачем.



---

## Інструкція із запуску

### 1. Підготовка бази даних
Переконайтеся, що MySQL сервер запущено. Створіть файл `.env` у кореневій директорії проєкту та додайте ваші дані:
```env
DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/finance_db```

Втсановлення всіх залежностей з файлу `requirements.txt`:
```bash
pip install -r requirements.txt```

Генерація CSV файлу
```bash 
python -m app.utils.csv_generator```

Запуск основного проекту
```bash
python -m main```