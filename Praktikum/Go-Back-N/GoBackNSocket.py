import csv
import sys
import time
from math import ceil
from lossy_udp_socket import lossy_udp_socket
from time import sleep
import os

def idToInt(id):
    while id.startswith("0") and len(id) > 1: id = id[1:]
    return int(id)


class GoBackNSocket():
    currentPackage = 0
    expectedPackage = 0
    windowMax = 0
    lastAck = 0

    receivedMsg = ""

    def __init__(self, localPort, remotePort, remoteAddress, PLR=0.1, segmentSize=1000, windowSize=1000, timeout=1, p=False):
        self.localPort = localPort
        self.remotePort = remotePort
        self.remoteAddress = remoteAddress
        self.sock = lossy_udp_socket(self, localPort, (remoteAddress, remotePort), PLR)
        self.segmentSize = segmentSize
        if self.segmentSize <= 4:
            self.segmentSize = 5
        self.windowSize = windowSize
        self.timeout = timeout
        GoBackNSocket.windowMax = self.windowSize - 1
        self.t = time.time()
        self.headerSize = 4
        self.p = p

    def send(self, msg):
        length = len(msg)
        numPackages = ceil(length / (self.segmentSize - self.headerSize))
        p = []
        for i in range(0, numPackages):
            id = str(i).zfill(self.headerSize)
            p.append(package(
                id + msg[i * (self.segmentSize - self.headerSize): (i + 1) * (self.segmentSize - self.headerSize)]))
        while self.currentPackage < numPackages:

            if time.time() > self.t + self.timeout or self.currentPackage == numPackages - 1:
                self.pprint(f"Package: {str(GoBackNSocket.expectedPackage)} timed out") if self.p else None
                GoBackNSocket.currentPackage = GoBackNSocket.expectedPackage

            if GoBackNSocket.currentPackage <= self.windowMax:
                d = str(p[GoBackNSocket.currentPackage].data[self.headerSize:]).replace('\n', ' ')
                self.sock.send(p[GoBackNSocket.currentPackage].data.encode("utf-8"))
                self.pprint(f"Sent package: {str(p[GoBackNSocket.currentPackage].id)} "f"pkg-data: {d}") if self.p else None
                self.t = time.time()
                GoBackNSocket.currentPackage += 1

    def receive(self, msg):
        msg = msg.decode('utf-8')
        id = idToInt(msg[:4])
        self.pprint("Received ack: " + str(id)) if self.p else None
        if id == GoBackNSocket.expectedPackage:
            GoBackNSocket.expectedPackage += 1
            GoBackNSocket.windowMax = id + self.windowSize + 1
            GoBackNSocket.receivedMsg = GoBackNSocket.receivedMsg + msg[4:]

    def pprint(self, text):
        string = text.ljust(150, ' ')
        string = string + str(f"current = {GoBackNSocket.currentPackage}, "
                              f"expected = {GoBackNSocket.expectedPackage}, "
                              f"windowMax = {self.windowMax}")
        print(string)
        sleep(0.001)


class package():
    def __init__(self, data):
        self.data = data
        self.id = idToInt(data[:4])


if __name__ == '__main__':
    try:
        os.remove("received.txt")
    except:
        pass

    if len(sys.argv) > 1:
        windowSize = int(sys.argv[1])
    else:
        windowSize = 256


    serverPort = 12000
    clientPort = 12001
    serverAdress = "127.0.0.1"
    clientAdress = "172.29.224.1"

    serverSocket = GoBackNSocket(serverPort, clientPort, serverAdress, 0.1, 1000, windowSize, 1)
    clientSocket = GoBackNSocket(clientPort, serverPort, serverAdress, 0.1, 1000, windowSize, 1)
    f = open("lotr.txt", "r")
    msg = f.read(257500)
    f.close()

    st = time.time()
    clientSocket.send(msg)

    # clientSocket.send(("0"*6+"1"*6+"2"*6+"3"*6+"4"*6+"5"*6+"6"*6+"7"*6+"8"*6+"9"*6)*10)
    # clientSocket.send("000000111111222222333333")
    # clientSocket.send("0000")

    sleep(1)
    et = time.time() - 1

    t = et - st
    serverSocket.sock.stop()
    with open("receivedLotr.txt", "w+") as fout:
        fout.write(GoBackNSocket.receivedMsg)
    clientSocket.sock.stop()

    csvFile = open("results.csv", "a", encoding="UTF8", newline='')
    writer = csv.writer(csvFile)
    writer.writerow([str(windowSize), t])