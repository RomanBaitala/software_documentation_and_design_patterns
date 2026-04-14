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

class FirestoreStrategy(StorageStrategy):
    def __init__(self, collection_name, project_id=None, service_account_file=None, credentials=None):
        from google.cloud import firestore
        client_kwargs = {}

        if service_account_file:
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_file(service_account_file)
            client_kwargs['credentials'] = creds
        elif credentials is not None:
            client_kwargs['credentials'] = credentials

        if project_id is not None:
            client_kwargs['project'] = project_id

        self.client = firestore.Client(**client_kwargs)
        self.collection = self.client.collection(collection_name)

    def write(self, data: list):
        print(f"[FIRESTORE] Збереження {len(data)} документів до колекції '{self.collection.id}'...")
        batch = self.client.batch()
        for row in data:
            doc_ref = self.collection.document()
            batch.set(doc_ref, row)
        batch.commit()

class DataExporter:
    """Контекст, який використовує стратегію"""
    def __init__(self, strategy: StorageStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StorageStrategy):
        self._strategy = strategy

    def export(self, data: list):
        self._strategy.write(data)