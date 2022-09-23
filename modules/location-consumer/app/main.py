import json
import os
from kafka import KafkaConsumer
from consumer.services import LocationService
from consumer.models import Location


TOPIC_NAME = 'location'
KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_SERVER = str(f'{KAFKA_URL}')
kafka_consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)


while True:
    
    for message in kafka_consumer:

        location_value = message.value
        location_value = json.loads(location_value.decode('utf-8'))
        print(location_value)
        location: Location = LocationService.create(location_value)
        print("Successfully Inserted!")