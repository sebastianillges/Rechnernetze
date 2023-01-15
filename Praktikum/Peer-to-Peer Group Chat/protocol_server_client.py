from client import Client
from utility import num_clients_to_int

class Protocol_Server_Client():

    def __init__(self, list, command):
        self.list = list
        self.command = command

    def get_encoded_package(self):
        encoded_msg = ""
        for c in self.list:
            encoded_msg = c.toString() + "|"
        encoded_msg = encoded_msg + self.command
        return encoded_msg.encode('utf-8')

    def get_decoded_package(msg: str):
        data_list = msg.split('|')
        client_list = []
        for i in range(0, len(data_list) - 1):
            client = data_list[i].split(',')
            client_list.append(Client(client[0], client[1], client[2]))
        return (data_list[len(data_list) - 1], client_list)

