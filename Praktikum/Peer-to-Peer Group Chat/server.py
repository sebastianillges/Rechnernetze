import socket
import sys
from threading import Thread, current_thread
from time import time, asctime
from socket import gethostbyname_ex, getfqdn
from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from protocol_broadcast import Protocol_Broadcast
from client import Client

class ServerThread(Thread):

    def __init__(self, conn, addr, server):
        Thread.__init__(self)
        self.sock = conn
        self.addr = addr
        self.server = server
        print (f"Server thread {current_thread().ident} connected to {addr[0]} via {addr[1]}")

    def run(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')                      # data is encoded
                if not data:                                        # receiving empty messages means that the socket other side closed the socket
                    sys.exit()
            except:
                print(f"Connection to {self.addr[0]} closed from outside")
                return

            # received data is of type Protocol_Client_Server because it can only come from a client
            msg_decoded = Protocol_Client_Server.get_decoded_package(data)
            self.eval_msg(msg_decoded)


    def eval_msg(self, msg: list):
        client = Client(msg[1], msg[2], msg[3])
        if msg[0] == "r":                                           # client wants to register
            Server.register(client, self.server.connection)
        elif msg[0] == "l":                                         # client wants to log out
            Server.logout(client)
        elif msg[0] == "b":
            Server.broadcast(self.server, msg)
        print(Server.client_list)


class Server():

    client_list = []
    connection_list = []

    def __init__(self, server_ip, server_port):
        self.serverIP = server_ip
        self.serverPort = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((server_ip, server_port))
        self.connection = socket.socket
        print(f'Server listening on Port {self.serverPort} for incoming TCP connections to IP {self.serverIP}')
        self.run()

    def run(self):
        while True:
            self.sock.listen(1)
            print('Listening ...')
            while True:
                try:
                    self.connection, addr = self.sock.accept()
                    print(f"Incoming connection accepted from {addr[0]} via {addr[1]}")
                    newthread = ServerThread(self.connection, addr, self)
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

        # send new client to all registered clients
        for c in Server.client_list:
            update_new_client = Protocol_Server_Client([client], "+").get_encoded_package()
            index = Server.client_list.index(c)
            con = Server.connection_list[index]
            con.send(update_new_client)

        # if not already registered add to global client list
        Server.client_list.append(client)
        print(f"Client with ip: {client_ip} registered!")
        Server.connection_list.append(connection)

        # send the List of all clients to the new registered client
        update_list_msg = Protocol_Server_Client(Server.client_list, "+").get_encoded_package()
        connection.send(update_list_msg)


    def logout(client: Client):
        # arg: client of type Client
        # removes client from global list (doesn't matter if exists or not)
        client_ip = client.get_ip()
        index = 0
        for c in Server.client_list:
            if c.get_ip() == client_ip:
                break
            index += 1
        print(f"{Server.client_list[index].get_nickname()} will sich verpissen")
        Server.client_list.pop(index)
        connection = Server.connection_list.pop(index)

        for c in Server.client_list:
            update_logout_client = Protocol_Server_Client([client], "-").get_encoded_package()
            index = Server.client_list.index(c)
            con = Server.connection_list[index]
            con.send(update_logout_client)

        print(f"Client {client_ip} logged out")
        connection.close()

    def broadcast(self, msg: list):
        # arg: list representation of decoded message received from a client
        # broadcasts the message to all registered clients
        paket = Protocol_Broadcast(msg[1], msg[4]).get_encoded_package()
        client_ip = msg[2]
        print(f"Client with ip: {client_ip} wants to broadcast \"{paket.decode('utf-8')}\"!")
        for c in Server.client_list:
            index = Server.client_list.index(c)
            connection = Server.connection_list[index]
            if not c.get_ip() == client_ip:
                connection.send(paket)
                print(f"Server broadcasting: \"{paket.decode('utf-8')}\" from {client_ip}!")