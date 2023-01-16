from sys import platform
from socket import gethostbyname_ex, getfqdn, gethostbyname, gethostname

def get_nickname_from_ip(ip: str, client_list):
    for c in client_list:
        if c.get_ip() == ip:
            return c.get_nickname()
    return "Unknown nickname"

def get_pc_ip():
    # Windows: get own IP with gethostbyname_ex(getfqdn())[2][0]
    # Mac: get own IP with gethostbyname(gethostname())
    if platform == "linux" or platform == "linux2" or platform == "darwin":  # linux or OS X
        peer_ip = gethostbyname(gethostname())
    elif platform == "win32":  # Windows...
        peer_ip = gethostbyname_ex(getfqdn())[2][0]
    else:
        peer_ip = "0"
        print("Could not recognize OS")
    return peer_ip