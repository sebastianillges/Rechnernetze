import threading
import time
from threading import Thread

class Station(Thread):
    def __init__(self, d, n):
        super().__init__()
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.busy = False
        self.CustomerWaitingEv = threading.Event()
        self.bufferLock = threading.Lock()
        self.busyLock = threading.Lock()
    def run(self):
        while 1:
            print("Station: " + self.name + " wartet auf Kunden")
            self.CustomerWaitingEv.wait()
            # kunde angekommen
            while self.busyLock.acquire() == False:
                time.sleep(0)
            self.busy = True
            time.sleep(self.buffer[0].getAnzahlItems() * self.delay_per_item)
            self.buffer[0].CustomerServingEv.set()
            self.buffer.pop(0)
            self.busyLock.release()

    def queue(self, customer):
        self.bufferLock.acquire()
        self.buffer.append(customer)
        print("Current buffer: " + str(self.buffer))
        self.bufferLock.release()
    def getBusy(self):
        return self.busy

    def getDelayPerItem(self):
        return self.delay_per_item


class Customer(Thread):
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0
    currentStation = "None"
    currentStatus = "not started"

    def __init__(self, ekList, name, startTime):
        super().__init__()
        self.ekList = ekList
        self.name = name
        self.startTime = startTime
        self.CustomerServingEv = threading.Event()
    def run(self):

        self.printStatus()
        time.sleep(self.startTime)

        while 1:
            if len(self.ekList) == 0:
                break

            # walking to station
            station = self.getStation()
            self.currentStatus = "otw to " + station.name
            self.printStatus()
            time.sleep(self.getWegzeit())

            self.currentStatus = "arrived at " + station.name
            self.currentStation = station.name
            self.printStatus()

            station.CustomerWaitingEv.set()

            if len(station.buffer) < self.getMaxQueueLen():
                station.queue(self)

    def getWegzeit(self):
        return self.ekList[0][0]

    def getStation(self):
        return self.ekList[0][1]

    def getAnzahlItems(self):
        return self.ekList[0][2]

    def getMaxQueueLen(self):
        return self.ekList[0][3]

    def printStatus(self):
        print("Kunde: " + self.name + " | Station: " + str(self.currentStation) + " | Status: " + str(self.currentStatus) + " | Time: " + str(simulation.getCurrentTime()))

class Sim:

    startTime = round(time.time())

    def getCurrentTime(self):
        return round(time.time() - self.startTime)


if __name__ == "__main__":

    simulation = Sim()


    baecker = Station(5, 'Bäcker')
    baecker.start()

    ekListTest = [(3, baecker, 2, 10)]


    kundeA1 = Customer(ekListTest, "A1", 1)
    kundeA1.start()

