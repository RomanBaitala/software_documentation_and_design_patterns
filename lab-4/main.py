import json
import os
from reader import CSVDataReader
from strategies import DataExporter, ConsoleStrategy, RedisStrategy, KafkaStrategy, FirestoreStrategy
from dotenv import load_dotenv

load_dotenv()

def resolve_env_vars(config):
    """Рекурсивно замінює значення, що починаються на $, на змінні оточення"""
    if isinstance(config, dict):
        for k, v in config.items():
            if isinstance(v, (dict, list)):
                resolve_env_vars(v)
            elif isinstance(v, str) and v.startswith('$'):
                env_key = v[1:]
                config[k] = os.getenv(env_key)
    return config

def main():
    if not os.path.exists('config.json'):
        print("Помилка: config.json не знайдено!")
        return

    with open('config.json', 'r') as f:
        config = resolve_env_vars(json.load(f))

    data = CSVDataReader.read(config['data_file'])
    if not data:
        print("Дані порожні.")
        return

    storage_type = config['storage_type']
    
    if storage_type == "console":
        strategy = ConsoleStrategy()
    elif storage_type == "redis":
        strategy = RedisStrategy(**config['redis'])
    elif storage_type == "kafka":
        strategy = KafkaStrategy(**config['kafka'])
    elif storage_type == "firestore":
        strategy = FirestoreStrategy(**config['firestore'])
    else:
        print("Невідомий тип сховища в конфігурації.")
        return

    exporter = DataExporter(strategy)
    exporter.export(data)

if __name__ == "__main__":
    main()