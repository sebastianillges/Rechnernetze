import socket

import socket
from threading import Thread
import random
from math import ceil
from lossy_udp_socket import lossy_udp_socket


class GoBackNSocket():
    currentSeg = 0

    def __init__(self, localPort, remotePort, remoteAddress, PLR=0.1, segmentSize=1000, windowSize=10):
        self.localPort = localPort
        self.remotePort = remotePort
        self.remoteAddress = remoteAddress
        self.sock = lossy_udp_socket(self, localPort, (remoteAddress, remotePort), PLR)
        self.segmentSize = segmentSize
        self.windowSize = windowSize


    def send(self, msg):
        length = len(msg)
        numSegments = ceil(length/ self.segmentSize)
        segments = []
        for i in range(0, numSegments):
            segments.append(msg[i * self.segmentSize : (i+1) * self.segmentSize])
        while(GoBackNSocket.currentSeg < numSegments)

    def receive(self, packet):

if __name__ == '__main__':
    serverPort = 12000
    clientPort = 12001
    serverSocket = GoBackNSocket(serverPort, clientPort, "localhost")

    clientSocket = GoBackNSocket(clientPort, serverPort, "127.0.0.96")
    clientSocket.send("ichbingay")
    sleep(1)
    serverSocket.lossy_udp_socket.stop()
    clientSocket.lossy_udp_socket.stop()