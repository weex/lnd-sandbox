# connect_open.py - connect to a peer and immediately open a channel of 1m sats
# Usage:
#    $ connect_open.py pubkey@ip

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import sys
from time import sleep

# Lnd cert is at ~/.lnd/tls.cert on Linux and
# ~/Library/Application Support/Lnd/tls.cert on Mac
cert = open(os.path.expanduser('~/.lnd/tls.cert')).read()
creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', creds)
stub = lnrpc.LightningStub(channel)


ls = lnrpc.LightningServicer()
if 1:
    n = sys.argv[1]
    pubkey, host = n.split('@')
    addr = ln.LightningAddress(pubkey=pubkey, host=host)
    request = ln.ConnectPeerRequest(addr=addr)
    try:
        response = stub.ConnectPeer(request)
    	print response
    except grpc._channel._Rendezvous as e:
        print "Error connecting to " + pubkey + ' ' + str(e)
        sys.exit()

    # try to open a channel to the new peer
    import codecs
    dest_hex = pubkey
    dest_bytes = codecs.decode(dest_hex, 'hex')

    request = ln.OpenChannelRequest(node_pubkey=dest_bytes,
                                    node_pubkey_string=pubkey,
                                    local_funding_amount=1000000)
    try:
        response = stub.OpenChannel(request)
	print response
        sleep(10)
	print response
    except grpc._channel._Rendezvous as e:
        print "Error opening channel with " + pubkey + ' ' + str(e)
                                

