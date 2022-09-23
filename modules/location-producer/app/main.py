import os
import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc


import json
from kafka import KafkaProducer


# Set up a Kafka producer
TOPIC_NAME = 'location'
KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_SERVER = str(f'{KAFKA_URL}')
print("KAFKA SERVER",KAFKA_SERVER)
kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            "id": int(request.id),
            "person_id": int(request.person_id),
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time
        }

        print(request_value)
        kafka_data = json.dumps(request_value).encode()
        kafka_producer.send(TOPIC_NAME, kafka_data)

        return location_pb2.LocationMessage(**request_value)



# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5555...")
server.add_insecure_port("[::]:5555")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)