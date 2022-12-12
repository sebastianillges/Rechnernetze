import socket
import struct
import time

def eval(op, N, zArray):
    result = 0
    if N != len(zArray):
        print("Argument N != number of elements")
        return
    operator = ""
    for c in op:
        if c.decode("utf-8") != " ":
            operator += c.decode("utf-8")
    if operator == "Summe" or operator == "+":
        for z in zArray:
            result += z
    elif operator == "Produkt" or operator == "*":
        result = 1
        for z in zArray:
            result *= z
    elif operator == "Minimum" or operator == "min":
        result = min(zArray)
    elif operator == "Maximum" or operator == "max":
        result = max(zArray)
    else:
        print("Invalid Operation " + operator)
    return result

My_IP = 'localhost'
My_PORT = 50000
server_activity_period = 30

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections')

t_end = time.time()+server_activity_period # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')

while 1 and time.time() < t_end:
    while time.time() < t_end:
        try:
            conn, addr = sock.accept()
            print('Incoming connection accepted: ', addr)
            break
        except socket.timeout:
            print('Socket timed out listening', time.asctime())

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
            datadecoded = struct.unpack("I" + "s" * 7 + "B" + "i" * int((dataSize - 12) / 4), data)
            datadecoded = (datadecoded[0], datadecoded[1:8], datadecoded[8], datadecoded[9:])

            print('received message: ', data, 'from ', addr, " decoded: ", datadecoded)
            result = eval(datadecoded[1], datadecoded[2], datadecoded[3])
            response = struct.pack("Ii", datadecoded[0], result)
            conn.send(response)

        except socket.timeout:
            print('Socket timed out at', time.asctime())

sock.close()
if conn:
    conn.close()
    print("Connection closed and timed out")