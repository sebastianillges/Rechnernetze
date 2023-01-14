from socket import socket, AF_INET, SOCK_STREAM
from time import asctime
from protocol_client_server import Protocol_Client_Server
from protocol_client_client import Protocol_Client_Client


class Peer():

    def __init__(self, nickname, ip, udp_port, tcp_port, server_ip, server_port):
        self.nickname = nickname
        self.ip = ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_list = []
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.register()

    def register(self):
        print(f"Trying to connect and register on server {self.server_ip} via port {self.server_port}")
        self.sock.connect((self.server_ip, self.server_port))
        paket = Protocol_Client_Server("r", self.nickname, self.ip, self.udp_port).get_encoded_package()
        self.sock.send(paket)
        try:
            msg = self.sock.recv(1024)
            msg = Protocol_Client_Server.get_decoded_package(msg)
            print('Message received; ', msg)
        except socket.timeout:
            print('Socket timed out at', asctime())
        self.sock.close()

    def logout(self):
        pass

    def broadcast(self):
        pass

    def send(self):
        pass