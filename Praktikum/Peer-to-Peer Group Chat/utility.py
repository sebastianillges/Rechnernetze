from sys import platform
from socket import gethostbyname_ex, getfqdn, gethostbyname, gethostname



def num_clients_to_int(id):
    while id.startswith("0") and len(id) > 1: id = id[1:]
    return int(id)



def get_pc_ip():
    if platform == "linux" or platform == "linux2" or platform == "darwin":  # linux or OS X
        peer_ip = gethostbyname(gethostname())
    elif platform == "win32":  # Windows...
        peer_ip = gethostbyname_ex(getfqdn())[2][0]
    else:
        peer_ip = "0"
        print("Could not recognize OS")
    return peer_ip