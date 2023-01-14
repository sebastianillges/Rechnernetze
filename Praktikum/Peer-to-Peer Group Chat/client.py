

class Client():

    def __init__(self, nickname, ip, udp_port):
        self.nickname = nickname
        self.ip = ip
        self.udp_port = udp_port

    def get_nickname(self):
        return self.nickname

    def get_ip(self):
        return self.ip

    def get_udp_port(self):
        return self.udp_port

    def toString(self):
        return(self.nickname + "," + self.ip + "," + self.udp_port)