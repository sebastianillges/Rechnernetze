from socket import *
from threading import Thread


class HybridServer(Thread):
    def __init__(self, server_port):
        Thread.__init__(self)
        self.server_port = server_port
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket.bind(('localhost', self.server_port))
        self.udp_socket.bind(('localhost', self.server_port))
        self.tcp_socket.listen(1)
        self.result = 0

    def run_udp(self):
        while True:
            message, clientAddress = self.udp_socket.recvfrom(2048)
            print('Server received: ', message.decode('utf-8'))
            self.udp_socket.sendto('200 OK'.encode('utf-8'), clientAddress)

            break
        self.udp_socket.close()

    def run_tcp(self):
        while True:
            connectionSocket, addr = self.tcp_socket.accept()
            msg = connectionSocket.recv(1024)
            print('Server received: ', msg.decode('utf-8'))
            connectionSocket.send("200 OK".encode('utf-8'))
            connectionSocket.close()
            break

    def run(self):
        udp_thread = Thread(target=self.run_udp)
        udp_thread.start()

        tcp_thread = Thread(target=self.run_tcp)
        tcp_thread.start()

        udp_thread.join()
        tcp_thread.join()


if __name__ == '__main__':
    s = HybridServer(50000)
    s.start()
