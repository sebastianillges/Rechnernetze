

class Protocol_Client_Request():

    def __init__(self, tcp_port, ip):
        self.command = "v"
        self.tcp_port = tcp_port
        self.ip = ip

    def get_encoded_package(self):
        encoded_msg = self.command + "|" + self.tcp_port + "|" + self.ip
        return encoded_msg.encode('utf-8')

    def get_decoded_package(msg: str):
        data_list = msg.split('|')
        return data_list
