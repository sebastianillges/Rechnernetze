import threading
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket
from threading import Thread

CONTINUE = True


# returns True if a connection can be made, False otherwise
def test_port_number(host, port):
    # create and configure the socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # set a timeout of a few seconds
        sock.settimeout(3)
        # connecting may fail
        try:
            # attempt to connect
            sock.connect((host, port))
            # a successful connection was made
            return True
        except:
            # ignore the failure
            return False


# scan port numbers on a host
def port_scan(host, port):
    print(f'Scanning {host}...')
    # scan each port number
    if test_port_number(host, port):
        print(f'> {host}:{port} open')


for i in range(1, 100):
    t = Thread(target=port_scan, args=('141.37.168.26', i))
    t.start()
