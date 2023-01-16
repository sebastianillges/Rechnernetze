from threading import enumerate
from utility import get_pc_ip
from server import Server
from peer import Peer
from sys import argv

def exit_handler(p):
    p.logout()

if __name__ == '__main__':
    server_port = 20000
    server_ip = get_pc_ip()

    #peer_ip = get_pc_ip()

    if len(argv) > 1:
        if argv[1] == "server":
            server = Server(server_ip, server_port)
        elif argv[1] == "peer":
            peer = Peer("peer", "192.168.0.208", 18201, 20001, server_ip, server_port, 21001)

    while True:
        command_input = input()
        if command_input == "logout":
            peer.logout()
            break
        elif command_input == "b":
            peer.broadcast(input())
        elif command_input == "s":
            peer.send_udp_request(input())
        elif command_input == "DEBUG":
            for thread in enumerate():
                print(thread.name)
        else:
            peer.send_p2p(command_input)