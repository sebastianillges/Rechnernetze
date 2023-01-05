import socket

import socket
from threading import Thread
import random
from math import ceil
from lossy_udp_socket import lossy_udp_socket


class go_back_n_socket():

    def __init__(self, localPort, remotePort, remoteAddress, PLR=0.1, segmentSize=1000, windowSize=10):
        self.localPort = localPort
        self.remotePort = remotePort
        self.remoteAddress = remoteAddress
        self.sock = lossy_udp_socket(self, localPort, (remoteAddress, remotePort), PLR)
        self.segmentSize = segmentSize
        self.windowSize = windowSize


    def send(self, msg):
        len = len(msg)
        numSeg = ceil(len/ self.segmentSize)
        msgSegments = []
        for i in range(numSeg):
            msgSegments.append(msg[i * self.segmentSize: (i + 1) * self.segmentSize])
            print('SOCK DEBUG | Message segments: ', msgSegments) if self.debugFlag else None

        # Send the message segments
        for i in range(numSeg):
            print('SOCK DEBUG | Sending segment: ', msgSegments[i]) if self.debugFlag else None
            self.sock.send(msgSegments[i].encode('utf-8'))

    def receive(self, packet):

