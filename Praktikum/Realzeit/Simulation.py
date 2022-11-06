import time
from threading import Thread, Lock, Event

class Station(Thread):
    def __init__(self, d, n):
        super().__init__()
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.busy = False
        self.CustomerWaitingEv = Event()
        self.bufferLock = Lock()
    def run(self):
        while 1:
            self.CustomerWaitingEv.wait()
            # kunde angekommen
            self.CustomerWaitingEv.clear()
            self.printStatus(self.name, "adding", self.buffer[0].name)
            self.printStatus(self.name, "serving", self.buffer[0].name)
            time.sleep((self.buffer[0].getAnzahlItems() * self.delay_per_item) / simulation.DEBUG)
            self.printStatus(self.name, "finished", self.buffer[0].name)
            self.buffer[0].CustomerServingEv.set()
            self.buffer.pop(0)

    def queue(self, customer):
        self.bufferLock.acquire()
        self.buffer.append(customer)
        #print("Current buffer: " + str(self.buffer))
        self.bufferLock.release()
    def getBusy(self):
        return self.busy

    def getDelayPerItem(self):
        return self.delay_per_item

    def printStatus(self, station, status, kunde):
        print(str(round(simulation.getCurrentTime())) + ":" + station + " " + status + " customer " + kunde)


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
        self.CustomerServingEv = Event()
    def run(self):

        time.sleep(self.startTime / simulation.DEBUG)
        while 1:
            # walking to station
            time.sleep(self.getWegzeit() / simulation.DEBUG)
            # customer arrived
            while len(self.ekList) > 0:
                station = self.getStation()
                if len(station.buffer) < self.getMaxQueueLen():
                    station.queue(self)
                    self.printStatus(self.name, "Queueing", station.name)
                    break
                else:
                    self.printStatus(self.name, "Dropped", station.name)
                    self.ekList.pop(0)
            if len(self.ekList) == 0:
                #print(self.name + " eklist empty")
                break

            station = self.getStation()
            station.CustomerWaitingEv.set()

            self.CustomerServingEv.wait()
            # customer gets served
            self.printStatus(self.name, "Finished", station.name)
            self.ekList.pop(0)
        # kunde DONE
        self.printStatus(self.name, "", " DONE")
        return

    def getWegzeit(self):
        return self.ekList[0][0]

    def getStation(self):
        return self.ekList[0][1]

    def getAnzahlItems(self):
        return self.ekList[0][2]

    def getMaxQueueLen(self):
        return self.ekList[0][3]

    def printStatus(self, kunde, status, station):
        print(str(round(simulation.getCurrentTime())) + ":" + kunde + " " + status + " at " + station)

class Sim:

    startTime = time.time()
    simDone = False
    DEBUG = 100

    def getCurrentTime(self):
        return (time.time() * simulation.DEBUG) - (self.startTime * simulation.DEBUG)


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        kunde.start()
        i += 1
        t += dT

if __name__ == "__main__":

    simulation = Sim()

    baeckerTest = Station(5, 'BäckerTest')
    baeckerTest.start()

    baecker = Station(10, 'Bäcker')
    baecker.start()
    metzger = Station(30, 'Metzger')
    metzger.start()
    kaese = Station(60, 'Käse')
    kaese.start()
    kasse = Station(5, 'Kasse')
    kasse.start()



    einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
    einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
    #startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
    #startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)

    ekListTest = [(3, baeckerTest, 2, 10)]
    kundeA1 = Customer(list(einkaufsliste1), "A1", 1)
    kundeA1.start()
    kundeA2 = Customer(list(ekListTest), "A2", 5)
    # kundeA2.start()

