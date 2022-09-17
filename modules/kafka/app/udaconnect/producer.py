import grpc
import location_pb2
import location_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from kafka import KafkaProducer

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""
def ReceiveLocation():
    timestamp = Timestamp()
    now = datetime.datetime.now()
    timestamp.FromDatetime(now)

    location = {
        "person_id":5,
        "longitude":-69.420,
        "latitude": 42.315,
        "creation_time": timestamp
    }
    return location

def PublishLocation():
    TOPIC_NAME = 'location'
    KAFKA_SERVER = 'localhost:9092'

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    location_object = ReceiveLocation()
    message = str(location_object)
    producer.send(TOPIC_NAME, message)
    producer.flush()

if __name__=="__main__":
    PublishLocation()