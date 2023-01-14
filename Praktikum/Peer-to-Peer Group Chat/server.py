import socket
from threading import Thread
from time import time, asctime
from socket import gethostbyname_ex, getfqdn
from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from client import Client

class ServerThread(Thread):

    def __init__(self, addr, conn):
        Thread.__init__(self)
        self.sock = conn
        print ("New connection added: ", addr)

    def run(self):
        while True:
            try:
                data = self.sock.recv(1024)                         # data is encoded
                if not data:                                        # receiving empty messages means that the socket other side closed the socket
                    print('Connection closed from other side')
                    print('Closing ...')
                    self.sock.close()
                    print("Connection closed")
                    # received data is of type Protocol_Client_Server because it can only come from a client
                    msg_decoded = Protocol_Client_Server.get_decoded_package(data)
                    self.eval_msg(msg_decoded)
            except socket.timeout:
                print('Socket timed out at', asctime())

    def eval_msg(msg: list):
        if msg[0] == "r":                                           # client wants to register
            Server.register(Client(msg[0], msg[1], msg[2]))
        elif msg[0] == "l":                                         # client wants to log out
            Server.logout(Client(msg[0], msg[1], msg[2]))
        elif msg[0] == "b":
            Server.broadcast(msg)





class Server():

    client_list = []

    def __init__(self, server_ip, server_port):
        self.serverIP = server_ip
        self.serverPort = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((server_ip, server_port))
        print('Listening on Port ', self.serverPort, ' for incoming TCP connections')
        self.run()

    def run(self):
        while True:

            self.sock.listen(1)
            print('Listening ...')

            while True:
                try:
                    conn, addr = self.sock.accept()
                    print('Incoming connection accepted: ', addr)
                    newthread = ServerThread(addr, conn)
                    newthread.start()
                except socket.timeout:
                    print('Socket timed out listening', asctime())

    def register(client: Client):
        # arg: client of type Client
        # check if client already registered
        client_ip = client.get_ip()
        for c in Server.client_list:
            if c.get_ip() == client_ip:
                print(f"Client with ip: {client_ip} already registered!")
                return
        # if not already registered add to global client list
        Server.client_list.append(client)

    def logout(client: Client):
        # arg: client of type Client
        # removes client from global list (doesn't matter if exists or not)
        Server.client_list.remove(client)

    def broadcast(msg: list):
        # arg: list representation of decoded message received from a client
        # broadcasts the message to all registered clients

        pass


if __name__ == '__main__':
    serverIP = gethostbyname_ex(getfqdn())[2][0]
    serverPort = 50000
    timeout = 300

    server = Server(serverIP, serverPort)
    server.run()