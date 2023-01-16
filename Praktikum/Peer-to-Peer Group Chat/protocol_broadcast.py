class Protocol_Broadcast():

    def __init__(self, name: str, msg):
        self.name = name
        self.msg = msg

    def get_encoded_package(self):
        encoded_msg = "b"
        encoded_msg = encoded_msg + "|" + self.name + "|" + self.msg
        return encoded_msg.encode('utf-8')

    def get_decoded_package(msg: str):
        data_list = msg.split('|')
        return data_list