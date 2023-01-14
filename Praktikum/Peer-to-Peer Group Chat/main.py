from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from client import Client
from server import Server
from socket import gethostbyname_ex, getfqdn

if __name__ == '__main__':

    server = Server(gethostbyname_ex(getfqdn())[2][0], 50000)

