import grpc
import location_pb2
import location_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from kafka import KafkaConsumer
import logging
from google.protobuf.json_format import MessageToDict

"""
Sample implementation of a kafka consumer that can be used to write messages to gRPC server.
"""

def ConsumeLocation():
    TOPIC_NAME = 'location'
    # KAFKA_SERVER = 'localhost:9092'
    KAFKA_SERVER = 'kafka.default.svc.cluster.local'
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

    channel = grpc.insecure_channel("127.0.0.1:5006", options=(('grpc.enable_http_proxy', 0),))
    stub = location_pb2_grpc.LocationServiceStub(channel)

    while True:
        try:
            for message in consumer:
                logging.info("message before persisting into db ...", message)
                # Send location data to db via gRPC server
                location_obj = MessageToDict(message)
                stub.Create(location_obj)
                logging.info("after calling LocationService...")
        except:
            print("Something went wrong while processing location messages...")
        finally:
            consumer.close()

if __name__=="__main__":
    ConsumeLocation()
