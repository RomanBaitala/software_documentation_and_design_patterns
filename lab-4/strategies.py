from abc import ABC, abstractmethod
import json

class StorageStrategy(ABC):
    @abstractmethod
    def write(self, data: list):
        pass

class ConsoleStrategy(StorageStrategy):
    def write(self, data: list):
        print("\n--- [CONSOLE OUTPUT] ---")
        for row in data[:5]:
            print(row)

class RedisStrategy(StorageStrategy):
    def __init__(self, host, port):
        import redis
        self.client = redis.Redis(host=host, port=port)

    def write(self, data: list):
        print(f"[REDIS] Запис {len(data)} рядків...")
        for row in data:
            self.client.rpush('salary_data', json.dumps(row))

class KafkaStrategy(StorageStrategy):
    def __init__(self, bootstrap_servers):
        from kafka import KafkaProducer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def write(self, data: list):
        print(f"[KAFKA] Відправка {len(data)} повідомлень...")
        for row in data:
            self.producer.send('salary_topic', row)
        self.producer.flush()

class DataExporter:
    """Контекст, який використовує стратегію"""
    def __init__(self, strategy: StorageStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StorageStrategy):
        self._strategy = strategy

    def export(self, data: list):
        self._strategy.write(data)