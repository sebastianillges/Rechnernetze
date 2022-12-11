import socket
import struct
import time

def eval(op, N, zArray):
    result = 0
    if N != len(zArray):
        print("Argument N != number of elements")
        return

    if op == "Summe" or op == "+":
        for z in zArray:
            result += z
    elif op == "Produkt" or op == "*":
        for z in zArray:
            result *= z
    elif op == "Minimum" or op == "min":
        result = min(zArray)
    elif op == "Maximum" or op == "max":
        result = max(zArray)
    else:
        print("Invalid Operation")
        result = None
    return result

My_IP = 'localhost'
My_PORT = 50000
server_activity_period = 30

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ',My_PORT, ' for incoming TCP connections')

t_end=time.time()+server_activity_period # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')

while 1 and time.time() < t_end:
    print("okö")
    while time.time() < t_end:
        try:
            conn, addr = sock.accept()
            print('Incoming connection accepted: ', addr)
            break
        except socket.timeout:
            print('Socket timed out listening',time.asctime())

    while time.time() < t_end:
        try:
            data = conn.recv(1024)
            if not data: # receiving empty messages means that the socket other side closed the socket
                print('Connection closed from other side')
                print('Closing ...')
                conn.close()
                print("Connection closed")
                break
            dataSize = len(bytes(data))
            datadecoded = struct.unpack("IsB" + "i" * int((dataSize - 8) / 4), data)
            # Des nur dass die zahlen wieder ein array sind
            zArray = datadecoded[3:]
            datadecoded = (datadecoded[0], datadecoded[1], datadecoded[2], zArray)
            print('received message: ', data, 'from ', addr, " decoded: ", datadecoded)


        except socket.timeout:
            print('Socket timed out at', time.asctime())

sock.close()
if conn:
    conn.close()
    print("Connection closed")