from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from utility import get_pc_ip
from client import Client
from server import Server
from peer import Peer
from time import sleep
from sys import argv

if __name__ == '__main__':
    # Windows: get own IP with gethostbyname_ex(getfqdn())[2][0]
    # Mac: get own IP with gethostbyname(gethostname())
    server_port = 50000
    #server_ip = "192.168.0.103"
    server_ip = "localhost"

    peer_ip = get_pc_ip()

    if len(argv) > 1:
        if argv[1] == "server":
            server = Server(server_ip, server_port)
        elif argv[1] == "peer":
            peer = Peer("peer", peer_ip, 5000, 5001, server_ip, server_port)

    sleep(1)
    peer.broadcast("test")
    sleep(1)
    peer.logout()