import csv

class CSVDataReader:
    @staticmethod
    def read(file_path):
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"Помилка: Файл {file_path} не знайдено.")
            return []