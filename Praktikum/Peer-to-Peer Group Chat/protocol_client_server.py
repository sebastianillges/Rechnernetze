class Protocol_Client_Server():

    def __init__(self, command, nickname, ip='', port='', msg=''):
        self.package = str(command + "|" + nickname + "|" + ip + "|" + str(port) + "|" + msg)

    def get_encoded_package(self):
        return self.package.encode('utf-8')

    def get_decoded_package(msg):
        packageDecoded = msg.decode('utf-8')
        dataList = packageDecoded.split('|')
        return dataList

