class Protocol_Client_Server():

    def __init__(self, command, nickname, ip='', port='', msg=''):
        self.package = str(command + "|" + nickname + "|" + ip + "|" + str(port) + "|" + msg)

    def get_encoded_package(self):
        return self.package.encode('utf-8')

    def get_decoded_package(msg: str):
        dataList = msg.split('|')
        return dataList

