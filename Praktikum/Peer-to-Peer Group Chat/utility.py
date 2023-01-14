class Utility():

    def num_clients_to_int(id):
        while id.startswith("0") and len(id) > 1: id = id[1:]
        return int(id)