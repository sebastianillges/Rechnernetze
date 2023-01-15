import threading
from socket import socket, AF_INET, SOCK_STREAM
from time import asctime
from protocol_client_server import Protocol_Client_Server
from protocol_client_client import Protocol_Client_Client
from time import sleep


class Peer():

    def __init__(self, nickname, ip, udp_port, tcp_port, server_ip, server_port):
        self.nickname = nickname
        self.ip = ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_list = []
        self.send_sock = socket(AF_INET, SOCK_STREAM)
        self.listen_sock = socket(AF_INET, SOCK_STREAM)
        self.register()
        self.newthread = threading.Thread

    def register(self):
        print(f"{self.nickname} trying to connect and register on server {self.server_ip} via port {self.tcp_port}")
        self.send_sock.connect((self.server_ip, self.server_port))
        paket = Protocol_Client_Server("r", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.send_sock.send(paket)
            print('Register successfully sent')
        except:
            print('Register failed')

    def logout(self):
        print(f"{self.nickname} trying to logout from server {self.server_ip} via port {self.tcp_port}")
        paket = Protocol_Client_Server("l", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.send_sock.send(paket)
            print('Logout successfully sent')
        except:
            print('Logout failed')

    def broadcast(self, msg: str):
        print(f"{self.nickname} trying to broadcast to server {self.server_ip} via port {self.tcp_port}")
        paket = Protocol_Client_Server("b", self.nickname, self.ip, self.udp_port, msg).get_encoded_package()
        try:
            self.send_sock.send(paket)
            print('Broadcast successfully sent')
        except:
            print('Broadcast failed')

    def send(self):
        pass

