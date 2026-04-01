import json
from reader import CSVDataReader
from strategies import DataExporter, ConsoleStrategy, RedisStrategy, KafkaStrategy

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    data = CSVDataReader.read(config['data_file'])
    if not data:
        return

    storage_type = config['storage_type']
    
    if storage_type == "console":
        strategy = ConsoleStrategy()
    elif storage_type == "redis":
        strategy = RedisStrategy(**config['redis'])
    elif storage_type == "kafka":
        strategy = KafkaStrategy(**config['kafka'])
    else:
        print("Невідомий тип сховища в конфігурації.")
        return

    exporter = DataExporter(strategy)
    exporter.export(data)

if __name__ == "__main__":
    main()