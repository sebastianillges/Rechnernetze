from socket import SOCK_STREAM, AF_INET, socket
from threading import Thread
from time import sleep


# returns True if a connection can be made, False otherwise
def test_port_number(host, port):
    # create a socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(2)
    # try to connect to the host
    try:
        print(sock.connect_ex((host, port)))
        return True
    except:
        return False


# scan port numbers on a host
def port_scan(host, port):
    # scan each port number
    if test_port_number(host, port):
        print(f'> {host}:{port} open')


print(f'Scanning 141.37.168.26...')
for i in range(1, 51):
    # create a thread for each port number
    sleep(0.1)
    t = Thread(target=port_scan, args=('141.37.168.26', i))
    t.start()
