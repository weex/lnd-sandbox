# lnd-sandbox
Random stuff with lnd + Python + GRPC

## Installation

ln\_stats.py requires that lnd is run with --no-macaroons and...

    pip install grpcio grpcio-tools googleapis-common-protos

If it still doesn't work, you might need to recompile the .proto files by following
http://dev.lightning.community/guides/python-grpc/
