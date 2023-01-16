

class Protocol_Client_Client():

    def __init__(self, command, data):
        self.command = command
        self.data = data

    def get_encoded_package(self):
        encoded_msg = str(self.command + "|" + self.data)
        return encoded_msg.encode('utf-8')

    def get_decoded_package(msg: str):
        data_list = msg.split('|')
        return data_list