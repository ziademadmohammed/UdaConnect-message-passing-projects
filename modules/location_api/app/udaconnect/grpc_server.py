import time
import logging
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc
from datetime import datetime
import location_service
from random import randint
import json

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        # Correct formatting of creation_time
        timestamp_dt = datetime.fromtimestamp(request.creation_time.seconds + request.creation_time.nanos /1e9)

        timestamp_st=timestamp_dt.strftime('%Y-%m-%d %H:%M:%S.%f')

        request_value = {
            "person_id":request.person_id,
            "creation_time":request.creation_time,
            "latitude": str(request.latitude),
            "longitude": str(request.longitude)
        }
        logging.info("request_value=", request_value)

        location_service.LocationService.Create(request_value)
        # return location_pb2.LocationMessageRequest(**request_value)

    def Retrieve(self, request, context):
        result_from_db = location_service.LocationService.Retrieve(request.id)

        if result_from_db:
            return location_pb2.LocationMessageResponse(
                id=result_from_db.id,
                person_id=result_from_db.person_id,
                coordinate=str(result_from_db.coordinate),
                creation_time=result_from_db.creation_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Location with id %s not found' % request.id)
            return location_pb2.Empty()

def serve():
    # Initialize gPRC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    logging.info("Server starting on port 5005...")

    server.add_insecure_port("[::]:5005")
    server.start()

    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()