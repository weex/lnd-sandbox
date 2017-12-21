import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import codecs

class LNDRPC:
    cert = open(os.path.expanduser('~/.lnd/tls.cert')).read()
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('localhost:10009', creds)
    stub = lnrpc.LightningStub(channel)
 
    def __init__(self):
        pass

    def get_balances(self):
        return self.stub.WalletBalance(ln.WalletBalanceRequest(witness_only=True))

    def describe_graph(self):
        return self.stub.DescribeGraph(ln.ChannelGraphRequest())

    def connect_peer(self, pubkey, host):
        addr = ln.LightningAddress(pubkey=pubkey, host=host)
        request = ln.ConnectPeerRequest(addr=addr)
        try:
            response = self.stub.ConnectPeer(request)
            return True
        except grpc._channel._Rendezvous as e:
            print "Error connecting to " + pubkey + ' ' + str(e)
            return False

    def open_channel(self, pubkey, local_funding_amount):
        pubkey_bytes = codecs.decode(pubkey, 'hex')

        request = ln.OpenChannelRequest(node_pubkey=pubkey_bytes,
                                        node_pubkey_string=pubkey,
                                        local_funding_amount=local_funding_amount)
        try:
            response = self.stub.OpenChannel(request)
            #TODO: return success when OpenChannel finishes
        except grpc._channel._Rendezvous as e:
            print "Error opening channel with " + pubkey + ' ' + str(e)


if __name__ == '__main__':
    l = LNDRPC()
    print l.describe_graph() 
