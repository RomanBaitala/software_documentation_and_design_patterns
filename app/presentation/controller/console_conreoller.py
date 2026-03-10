from ..interfaces.iapp_controller import IAppController
from ...bll.services.import_data_from_csv import DataImportService

class ConsoleController(IAppController):
    def __init__(self, import_service: DataImportService):
        self.import_service = import_service

    def run_import(self):
        print("Початок імпорту даних з CSV...")
        try:
            count = self.import_service.import_all_from_csv()
            print(f"Імпорт завершено! Оброблено {count} рядків.")
        except Exception as e:
            print(f"Помилка під час імпорту: {e}")

    def show_stats(self):
        print("Статистика системи: Дані успішно синхронізовано з БД.")