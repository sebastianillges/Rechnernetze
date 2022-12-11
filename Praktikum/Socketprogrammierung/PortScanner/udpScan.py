import random
import socket
import struct
from threading import Thread


class SendDNSPkt:
    def __init__(self, url, serverIP, port=1):
        self.url = url
        self.serverIP = serverIP
        self.port = port

    def sendPkt(self):
        pkt = self._build_packet()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(bytes(pkt), (self.serverIP, self.port))
        data, addr = sock.recvfrom(1024)
        sock.close()
        return data

    def _build_packet(self):
        randint = random.randint(1, 50)
        packet = struct.pack(">H", randint)  # Query Ids (Just 1 for now)
        packet += struct.pack(">H", 0x0100)  # Flags
        packet += struct.pack(">H", 1)  # Questions
        packet += struct.pack(">H", 0)  # Answers
        packet += struct.pack(">H", 0)  # Authorities
        packet += struct.pack(">H", 0)  # Additional
        split_url = self.url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for s in part:
                packet += struct.pack('c', s.encode())
        packet += struct.pack("B", 0)  # End of String
        packet += struct.pack(">H", 1)  # Query Type
        packet += struct.pack(">H", 1)  # Query Class
        return packet


def checkDNSPortOpen(port):
    # replace 8.8.8.8 with your server IP!

    s = SendDNSPkt('www.google.com', '141.37.168.26', port)
    portOpen = False
    for _ in range(5):  # udp is unreliable.Packet loss may occur
        try:
            s.sendPkt()
            portOpen = True
            break
        except socket.timeout:
            pass
    if portOpen:
        print('port open!')
    else:
        print('port closed!')


if __name__ == '__main__':
    for i in range(1, 50):
        t = Thread(target=checkDNSPortOpen, args=(i,))
        t.start()
