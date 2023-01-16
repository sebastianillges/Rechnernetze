import sys
import threading
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import asctime
from protocol_client_server import Protocol_Client_Server
from protocol_client_client import Protocol_Client_Client
from protocol_server_client import Protocol_Server_Client
from protocol_broadcast import Protocol_Broadcast
from protocol_client_request import Protocol_Client_Request
from client import Client
from time import sleep

class Peer():

    def __init__(self, nickname, ip, udp_port, tcp_port, server_ip, server_port, p2p_port):
        self.print_lock = threading.Lock()
        self.LOGGEDIN = False
        self.CONNECTEDTOCLIENT = False
        self.INITIATOR = None
        self.nickname = nickname
        self.ip = ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.p2p_port = p2p_port
        self.client_list = []
        self.p2p_addr = ""
        self.p2p_connection = socket
        self.p2p_nickname = ""
        self.tcp_sock = socket(AF_INET, SOCK_STREAM)
        self.tcp_sock_p2p = socket(AF_INET, SOCK_STREAM)
        self.udp_sock_receive = socket(AF_INET, SOCK_DGRAM)
        self.udp_sock_send = socket(AF_INET, SOCK_DGRAM)
        self.register()
        self.tcp_thread = threading.Thread(target=self.listen_tcp_server).start()
        self.udp_thread = threading.Thread(target=self.listen_udp_request).start()

    def register(self):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to connect and register on server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        self.tcp_sock.connect((self.server_ip, self.server_port))
        paket = Protocol_Client_Server("r", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.tcp_sock.send(paket)
            self.print_lock.acquire()
            print('Register successfully sent')
            self.print_lock.release()
            self.LOGGEDIN = True
        except:
            self.print_lock.acquire()
            print('Register failed')
            self.print_lock.release()
        sleep(1)

    def logout(self):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to logout from server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        paket = Protocol_Client_Server("l", self.nickname, self.ip, self.udp_port).get_encoded_package()
        try:
            self.tcp_sock.send(paket)
            self.print_lock.acquire()
            print('Logout successfully sent')
            self.print_lock.release()
            self.LOGGEDIN = False
        except:
            self.print_lock.acquire()
            print('Logout failed')
            self.print_lock.release()
        sleep(1)
        self.tcp_sock.close()

    def broadcast(self, msg: str):
        self.print_lock.acquire()
        print(f"{self.nickname} trying to broadcast to server {self.server_ip} via port {self.tcp_port}")
        self.print_lock.release()
        paket = Protocol_Client_Server("b", self.nickname, self.ip, self.udp_port, msg).get_encoded_package()
        try:
            self.tcp_sock.send(paket)
            self.print_lock.acquire()
            print('Broadcast successfully sent')
            self.print_lock.release()
        except:
            self.print_lock.acquire()
            print('Broadcast failed')
            self.print_lock.release()
        sleep(1)

    def listen_tcp_server(self):
        while True:
            try:
                data = self.tcp_sock.recv(1024).decode('utf-8')
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
        self.listen_tcp_server()

    def send_udp_request(self, nickname):
        # p2p initiator sends udp request to target with nickname
        self.p2p_nickname = nickname
        print(f"{self.nickname} sending udp request to {self.p2p_nickname}")
        client_ip = ""
        client_port = 0
        for c in self.client_list:
            if c.get_nickname() == self.p2p_nickname:
                client_ip = str(c.get_ip())
                client_port = int(c.get_udp_port())
        request = Protocol_Client_Request(str(self.p2p_port), self.ip).get_encoded_package()
        self.udp_sock_send.sendto(request, (client_ip, client_port))
        # p2p initiator starts a tcp connection as a server
        threading.Thread(target=self.start_p2p).start()

    def listen_udp_request(self):
        self.udp_sock_receive.bind((self.ip, self.udp_port))
        print(f"Bind({self.ip, self.udp_port}")
        while True:
            try:
                data, addr = self.udp_sock_receive.recvfrom(1024)
                data = data.decode('utf-8')
                self.eval_msg(data)
                break
            except socket.timeout:
                print('Socket timed out at', asctime())
        self.listen_udp_request()

    def start_p2p(self):
        # p2p initiator acts as server of a p2p tcp connection
        print(f"{self.nickname} initiating tcp connection to {self.p2p_nickname}")
        self.tcp_sock_p2p.bind((self.ip, self.p2p_port))
        self.tcp_sock_p2p.listen(1)
        while True:
            try:
                self.p2p_connection, self.p2p_addr = self.tcp_sock_p2p.accept()
                print(f"{self.nickname} accepted incoming p2p connection from {self.p2p_nickname}")
                self.INITIATOR = True
                break
            except socket.timeout:
                print('Socket timed out listening', asctime())
        threading.Thread(target=self.listen_p2p).start()
    def connect_p2p(self, addr, port):
        self.tcp_sock_p2p.connect((str(addr), int(port)))
        self.INITIATOR = False

    def listen_p2p(self):
        while True:
                try:
                    if self.INITIATOR:
                        msg = self.p2p_connection.recv(1024).decode('utf-8')
                        if not msg:
                            break
                    elif not self.INITIATOR:
                        msg = self.tcp_sock_p2p.recv(1024).decode('utf-8')
                    print('Message received; ', msg)
                except socket.timeout:
                    print('Socket timed out at', asctime())
        self.listen_p2p()

    def send_p2p(self, msg: str):
        print(self.INITIATOR)
        if self.INITIATOR:
            print(f"initiator send")
            self.p2p_connection.send(msg.encode('utf-8'))
        elif not self.INITIATOR:
            print(f"target send")
            self.tcp_sock_p2p.send(msg.encode('utf-8'))

    def eval_msg(self, data):
        if data[0] == "b":                                          # broadcast message
            msg = Protocol_Broadcast.get_decoded_package(data)
            self.print_lock.acquire()
            print(f"Received message from {msg[1]}: {msg[2]}")
            self.print_lock.release()
        elif data[0] == "v":                                        # p2p connection setup via udp
            msg = Protocol_Client_Request.get_decoded_package(data)
            self.connect_p2p(msg[2], int(msg[1]))                   # msg[1] = port, msg[2] = addr
            threading.Thread(target=self.listen_p2p())
        #elif data[0] == "s":                                        # p2p message
        #    msg = Protocol_Client_Client.get_decoded_package(data)
        #    self.send_p2p(msg[1])                                   # only send data portion of protocol
        else:
            operatror, list = Protocol_Server_Client.get_decoded_package(data)
            if operatror == "+":
                self.print_lock.acquire()
                for c in list:
                    print(f"{c.get_nickname()} is logged in")
                    self.client_list.append(c)
                self.print_lock.release()
            elif operatror == "-":
                self.print_lock.acquire()
                print(f"{list[0].get_nickname()} logged out")
                self.print_lock.release()
                self.client_list.remove(list[0])