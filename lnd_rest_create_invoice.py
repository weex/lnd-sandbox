import base64, codecs, json
import requests, os

LND_DIR = os.path.expanduser('~/.lnd/')

url = 'https://localhost:8080/v1/invoices'
cert_path = LND_DIR + '/tls.cert'
macaroon = codecs.encode(open(LND_DIR + '/data/chain/bitcoin/mainnet/invoice.macaroon', 'rb').read(), 'hex')

headers = {'Grpc-Metadata-macaroon': macaroon}

#os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

data = { 
#        'route_hints': <array RouteHint>, 
#        'fallback_addr': <string>, 
#        'r_hash': base64.b64encode(<byte>).decode(), 
#        'settle_date': <string>, 
        'expiry': '3600', 
        'memo': "This is a test", 
#        'receipt': base64.b64encode(<byte>).decode(), 
#        'settle_index': <string>, 
#        'add_index': <string>, 
#        'payment_request': <string>, 
        'value': '1000'
#        'settled': <boolean>, 
#        'amt_paid_msat': <string>, 
#        'amt_paid': <string>, 
#        'amt_paid_sat': <string>, 
#        'private': <boolean>, 
#        'creation_date': <string>, 
#        'description_hash': base64.b64encode(<byte>).decode(), 
#        'r_preimage': base64.b64encode(<byte>).decode(), 
#        'cltv_expiry': <string>, 
    }

r = requests.post(url, headers=headers, verify=cert_path, data=json.dumps(data))
try:
    print(r.json())
    data = r.json()
    import qrcode

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(data['payment_request'])
    qr.print_ascii(invert=True)
    print "Please pay: " + data['payment_request']
    
except:
    print("not json: " + r.text)

