from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from client import Client
from server import Server
from peer import Peer
from socket import gethostbyname_ex, getfqdn, gethostbyname, gethostname
from sys import platform

if __name__ == '__main__':
    # Windows: get own IP with gethostbyname_ex(getfqdn())[2][0]
    # Mac: get own IP with gethostbyname(gethostname())

    server_port = 50000
    server_ip = "192.168.0.103"

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # linux or OS X
        server = Server(gethostbyname(gethostname()), server_port)
        peer = Peer("laptop", gethostbyname(gethostname()), 5000, 5001, server_ip, server_port)
    elif platform == "win32":
        # Windows...
        #server = Server(gethostbyname_ex(getfqdn())[2][0], server_port)
        peer = Peer("laptop", gethostbyname_ex(getfqdn())[2][0], 5000, 50000, server_ip, server_port)

