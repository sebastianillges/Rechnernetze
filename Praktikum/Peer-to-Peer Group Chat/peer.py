import sys
import threading
from socket import socket, AF_INET, SOCK_STREAM
from time import asctime
from protocol_client_server import Protocol_Client_Server
from protocol_client_client import Protocol_Client_Client
from protocol_server_client import Protocol_Server_Client
from protocol_broadcast import Protocol_Broadcast
from time import sleep


class Peer():

    def __init__(self, nickname, ip, udp_port, tcp_port, server_ip, server_port):
        self.print_lock = threading.Lock()
        self.LOGGEDIN = False
        self.nickname = nickname
        self.ip = ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_list = []
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.register()
        self.newthread = threading.Thread(target=self.listen).start()

    def register(self):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to connect and register on server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        self.sock.connect((self.server_ip, self.server_port))
        paket = Protocol_Client_Server("r", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.sock.send(paket)
            self.print_lock.acquire()
            print('Register successfully sent')
            self.print_lock.release()
            self.LOGGEDIN = True
        except:
            self.print_lock.acquire()
            print('Register failed')
            self.print_lock.release()
        sleep(1)
        print(self.sock)

    def logout(self):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to logout from server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        paket = Protocol_Client_Server("l", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.sock.send(paket)
            self.print_lock.acquire()
            print('Logout successfully sent')
            self.print_lock.release()
            self.LOGGEDIN = False
        except:
            self.print_lock.acquire()
            print('Logout failed')
            self.print_lock.release()
        sleep(1)
        print(self.sock)
        self.sock.close()

    def broadcast(self, msg: str):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to broadcast to server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        paket = Protocol_Client_Server("b", self.nickname, self.ip, self.udp_port, msg).get_encoded_package()
        try:
            self.sock.send(paket)
            self.print_lock.acquire()
            print('Broadcast successfully sent')
            self.print_lock.release()
        except:
            self.print_lock.acquire()
            print('Broadcast failed')
            self.print_lock.release()
        sleep(1)

    def listen(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:                                        # receiving empty messages means that the socket other side closed the socket
                    sys.exit()
                else:
                    threading.Thread(target=self.eval_msg(data)).start()
                    break
            except:
                if self.LOGGEDIN:
                    break
                self.print_lock.acquire()
                print(f"{self.ip} stopped listening")
                self.print_lock.release()
                return
        self.listen()

    def eval_msg(self, data):
        if data[0] == "b":
            msg = Protocol_Broadcast.get_decoded_package(data)
            self.print_lock.acquire()
            print(f"Received message from {msg[1]}: {msg[2]}")
            self.print_lock.release()
        else:
            operatror, list = Protocol_Server_Client.get_decoded_package(data)
            if operatror == "+":
                self.print_lock.acquire()
                for c in list:
                    print(f"{c.get_nickname()} is logged in")
                self.client_list.append(list)
                self.print_lock.release()
            elif operatror == "-":
                self.print_lock.acquire()
                print(f"{list[0].get_nickname()} logged out")
                self.print_lock.release()
                self.client_list.remove(list[0])

    def send(self):
        pass

