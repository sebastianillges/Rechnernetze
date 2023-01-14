import socket
from threading import Thread
from time import time, asctime
from socket import gethostbyname_ex, getfqdn
from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from client import Client

class ServerThread(Thread):

    def __init__(self, addr, conn, server):
        Thread.__init__(self)
        self.sock = conn
        self.addr = addr
        self.server = server
        print (f"Server thread {self.ident} connected to {addr[0]} via {addr[1]}")

    def run(self):
        data = ""
        while True:
            try:
                data = self.sock.recv(1024)                         # data is encoded
                if not data:                                        # receiving empty messages means that the socket other side closed the socket
                    self.sock.close()
                    print(f"{self.addr[0]} closed the connection")
                    break
            except socket.timeout:
                print('Socket timed out at', asctime())

            # received data is of type Protocol_Client_Server because it can only come from a client
            msg_decoded = Protocol_Client_Server.get_decoded_package(data)
            self.eval_msg(msg_decoded)


    def eval_msg(self, msg: list):
        if msg[0] == "r":                                           # client wants to register
            Server.register(Client(msg[0], msg[1], msg[2]), self.sock)
        elif msg[0] == "l":                                         # client wants to log out
            Server.logout(Client(msg[0], msg[1], msg[2]))
        elif msg[0] == "b":
            Server.broadcast(self.server,msg)


class Server():

    client_list = []
    connection_list = []

    def __init__(self, server_ip, server_port):
        self.serverIP = server_ip
        self.serverPort = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((server_ip, server_port))
        self.connection = socket.socket
        print(f'Listening on Port {self.serverPort} for incoming TCP connections to IP {self.serverIP}')
        self.run()

    def run(self):
        while True:

            self.sock.listen(1)
            print('Listening ...')

            while True:
                try:
                    self.connection, addr = self.sock.accept()
                    con = self.connection
                    print(f"Incoming connection accepted from {addr[0]} via {addr[1]}")
                    newthread = ServerThread(addr, con, self)
                    newthread.start()
                except socket.timeout:
                    print('Socket timed out listening', asctime())

    def register(client: Client, connection: socket.socket):
        # arg: client of type Client
        # check if client already registered
        client_ip = client.get_ip()
        for c in Server.client_list:
            if c.get_ip() == client_ip:
                print(f"Client with ip: {client_ip} already registered!")
                return
        # if not already registered add to global client list
        Server.client_list.append(client)
        Server.connection_list.append(connection)

    def logout(client: Client):
        # arg: client of type Client
        # removes client from global list (doesn't matter if exists or not)
        index = Server.client_list.index(client)
        Server.client_list.remove(client)
        Server.connection_list.pop(index)

    def broadcast(self, msg: list):
        # arg: list representation of decoded message received from a client
        # broadcasts the message to all registered clients
        client_ip = msg[2]
        client_port = msg[3]
        paket = msg[4].encode('utf-8')
        for c in Server.client_list:
            index = Server.client_list.index(c)
            connection = Server.connection_list[index]
            #if not c.get_ip() == client_ip:
            connection.send(paket)