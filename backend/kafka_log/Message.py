from datetime import datetime
import json
from kafka import KafkaProducer


class Message:
    """Class message to Kafka"""
    @staticmethod
    async def log_action(action: str, user_id: int = None):
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        message = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        producer.send('tariff_changes_topic', json.dumps(message).encode('utf-8'))
        producer.flush()
        producer.close()
