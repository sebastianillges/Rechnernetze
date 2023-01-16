import atexit
from socket import socket, AF_INET, SOCK_DGRAM
from protocol_client_server import Protocol_Client_Server
from protocol_server_client import Protocol_Server_Client
from utility import get_pc_ip
from client import Client
from server import Server
from peer import Peer
from time import sleep
from sys import argv
#import atexit

def exit_handler(self):
    self.logout()

if __name__ == '__main__':
    server_port = 20000
    server_ip = get_pc_ip()

    #peer_ip = get_pc_ip()

    if len(argv) > 1:
        if argv[1] == "server":
            server = Server(server_ip, server_port)
        elif argv[1] == "peer":
            peer = Peer("peer", "192.168.0.208", 18201, 20001, server_ip, server_port)

    #atexit.register(exit_handler(peer))
    peer.broadcast("test")

    while True:
        command_input = input()
        if command_input == "logout":
            peer.logout()
        elif command_input == "b":
            peer.broadcast(input())
        elif command_input == "s":
            peer.send_udp_request(input())
        else:
            peer.send_p2p(command_input)