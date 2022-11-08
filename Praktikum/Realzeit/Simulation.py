import threading
import time
from threading import Thread


class Station(Thread):
    def __init__(self, d, n):
        super().__init__()
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.CustomerWaiting = False
        self.busy = False
        self.cond = threading.Condition()
        self.start()
    def run(self):
        self.cond.wait()




class Customer(Thread):
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    def __init__(self, ekList, name, startTime):
        super().__init__()
        self.ekList = ekList
        self.name = name
        self.startTime = startTime
        self.start()
    def run(self):
        time.wait(self.startTime)
        while():
            station = self.ekList[0][1]
            time.wait(self.eckList[0][0])
            if (station.cond.acquire()):
                time = (self.eckList[0][2] * station.delay_per_item)
                time.wait(time)
                station.cond.wait(time)
                station.busy = True
            else:








def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        i += 1
        t += dT

if __name__ == "__main__":
    baecker = Station(10, 'Bäcker')
    metzger = Station(30, 'Metzger')
    kaese = Station(60, 'Käse')
    kasse = Station(5, 'Kasse')
    Customer.served['Bäcker'] = 0
    Customer.served['Metzger'] = 0
    Customer.served['Käse'] = 0
    Customer.served['Kasse'] = 0
    Customer.dropped['Bäcker'] = 0
    Customer.dropped['Metzger'] = 0
    Customer.dropped['Käse'] = 0
    Customer.dropped['Kasse'] = 0
    einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
    einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
    startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
    startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)