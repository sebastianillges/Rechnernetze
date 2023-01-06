import time
from math import ceil
from lossy_udp_socket import lossy_udp_socket


def idToInt(id):
    while id.startswith("0") and len(id) > 1: id = id[1:]
    return int(id)


class GoBackNSocket():
    currentSeg = 0

    def __init__(self, localPort, remotePort, remoteAddress, PLR=0.1, segmentSize=1000, windowSize=10):
        self.localPort = localPort
        self.remotePort = remotePort
        self.remoteAddress = remoteAddress
        self.sock = lossy_udp_socket(self, localPort, (remoteAddress, remotePort), PLR)
        self.segmentSize = segmentSize
        if self.segmentSize <= 4:
            self.segmentSize = 5
        self.windowSize = windowSize


    def send(self, msg):
        length = len(msg)
        numPackages = ceil(length / (self.segmentSize - self.headerSize))
        p = []
        for i in range(0, numPackages):
            id = str(i).zfill(self.headerSize)
            p.append(package(
                id + msg[i * (self.segmentSize - self.headerSize): (i + 1) * (self.segmentSize - self.headerSize)]))
        while self.currentPackage < numPackages:
            # print(str(self.currentPackage) + ", " + str(self.expectedPackage))
            # print(str(time.time()) + ", " + str(self.t + self.timeout))
            sleep(0.05)
            # print(f"current = {GoBackNSocket.currentPackage}, expected = {GoBackNSocket.expectedPackage}")
            if time.time() > self.t + self.timeout:
                self.pprint(f"Package: {str(GoBackNSocket.expectedPackage)} timed out")
                GoBackNSocket.currentPackage = GoBackNSocket.expectedPackage

            if GoBackNSocket.currentPackage <= self.windowMax:
                self.sock.send(p[GoBackNSocket.currentPackage].data.encode("utf-8"))
                self.pprint(f"Sent package: {str(p[GoBackNSocket.currentPackage].id)} "
                            f"pkg-data: {str(p[GoBackNSocket.currentPackage].data[self.headerSize:])}")
                sleep(0.001)
                self.t = time.time()
                GoBackNSocket.currentPackage += 1

    def receive(self, msg):
        msg = msg.decode('utf-8')
        id = idToInt(msg[:4])
        self.pprint("Received ack: " + str(id))
        if id == GoBackNSocket.expectedPackage:
            GoBackNSocket.expectedPackage += 1
            if GoBackNSocket.currentPackage == GoBackNSocket.windowMax - 1:
                GoBackNSocket.windowMax = id + self.windowSize

    def pprint(self, text):
        string = text.ljust(60, ' ')
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
    serverPort = 12000
    clientPort = 12001
    serverAdress = "127.0.0.1"
    clientAdress = "172.29.224.1"

    serverSocket = GoBackNSocket(serverPort, clientPort, serverAdress, 0.1)
    clientSocket = GoBackNSocket(clientPort, serverPort, serverAdress, 0.1)

    clientSocket.send(("0"*6+"1"*6+"2"*6+"3"*6+"4"*6+"5"*6+"6"*6+"7"*6+"8"*6+"9"*6)*10)
    # clientSocket.send("000000111111222222333333")

    sleep(1)
    serverSocket.sock.stop()
    clientSocket.sock.stop()
