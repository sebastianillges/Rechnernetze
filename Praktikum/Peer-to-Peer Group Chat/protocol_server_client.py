from client import Client
from utility import Utility

class Protocol_Server_Client():

    def __init__(self, numClients, list):
        self.numClients = numClients
        self.list = list

    def get_encoded_package(self):
        encoded_msg = ""
        id = str(self.numClients).zfill(4)
        encoded_msg = encoded_msg + id
        for c in self.list:
            encoded_msg = encoded_msg + "|" + c.toString()
        return encoded_msg.encode('utf-8')

    def get_decoded_package(msg):
        packageDecoded = msg.decode('utf-8')
        data_list = packageDecoded.split('|')
        num_clients = Utility.num_clients_to_int(data_list[0])
        client_list = [num_clients]
        for i in range(1, len(data_list)):
            client = data_list[i].split(',')
            client_list.append(Client(client[0], client[1], client[2]))
        return client_list

