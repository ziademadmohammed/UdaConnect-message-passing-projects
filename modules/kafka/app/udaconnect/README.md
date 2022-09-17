## Generating gRPC files
pip install grpcio-tools grpcio

# The path ./ can be replaced with another path or an absolute path to your .proto file
python3 -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto