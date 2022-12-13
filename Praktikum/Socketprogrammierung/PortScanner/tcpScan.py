from socket import SOCK_STREAM, AF_INET, socket
from threading import Thread
from time import sleep


# returns True if a connection can be made, False otherwise
def test_port_number(host, port):
    # create a socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setblocking(False)
    sock.settimeout(10)
    # try to connect to the host
    result = sock.connect_ex((host, port))
    sock.close()
    return result



# scan port numbers on a host
def port_scan(host, port):
    # scan each port number
    res = test_port_number(host, port)
    if res == 0:
        print(f'> {host}:{port} open')
    elif res == 61:
        print(f'> {host}:{port} connecting restricted')
    elif res == 60:
        print(f'> {host}:{port} closed')
    else:
        print(f'> {host}:{port} %d' % res)


print(f'Scanning 141.37.168.26...')
for i in range(1, 51):
    # create a thread for each port number
    sleep(0.1)
    t = Thread(target=port_scan, args=('141.37.168.26', i))
    t.start()
