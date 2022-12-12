import socket
import struct
import time

Server_IP = 'localhost'
Server_PORT = 50000
id = 1
operator = "+"
operator = '{message: <7}'.format(message=operator)
print(operator)
operatorBytes = []
for c in operator:
    operatorBytes.append(c.encode())
N = 3
zArray = (1, 2, 3)
requestdecoded = (id, operatorBytes, N, zArray)
if requestdecoded[2] != len(requestdecoded[3]):
    print("Argument N != number of elements")
request = struct.pack("I" + "s" * 7 + "B" + "i" * requestdecoded[2], requestdecoded[0], *requestdecoded[1], requestdecoded[2], *requestdecoded[3])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))
print(sock.getsockname())
print('Sending message', request, " decoded: ", requestdecoded)
sock.send(request)
try:
    msg = sock.recv(1024)
    print('Message received; ', msg, " decoded: " + str(struct.unpack("Ii", msg)))
except socket.timeout:
    print('Socket timed out at', time.asctime())
sock.close()