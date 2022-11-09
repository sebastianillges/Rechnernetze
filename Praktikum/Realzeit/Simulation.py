import os.path
import sys
import time
from threading import Thread, Lock, Event

f = open(os.path.join(sys.path[0], "supermarkt.txt"), "w")
fc = open(os.path.join(sys.path[0], "supermarkt_customer.txt"), "w")
fs = open(os.path.join(sys.path[0], "supermarkt_station.txt"), "w")

allCustomers = []

# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, s, msg):
    t = simulation.getCurrentTime()
    print(str(round(t)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(s, msg, name):
    t = simulation.getCurrentTime()
    print(str(round(t))+':'+s+' '+msg)
    fs.write(str(round(t)) + ':' + s + ' ' + msg + ' ' + name + '\n')

class Station(Thread):
    def __init__(self, d, n):
        super().__init__()
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.busy = False
        self.CustomerWaitingEv = Event()
        self.bufferLock = Lock()
        #self.busyLock = Lock()
    def run(self):
        while 1:
            self.CustomerWaitingEv.wait()
            # kunde angekommen
            self.CustomerWaitingEv.clear()
            my_print2(self.name, "adding", self.buffer[0].name)
            my_print2(self.name, "serving", self.buffer[0].name)
            time.sleep((self.buffer[0].getAnzahlItems() * self.delay_per_item) / simulation.DEBUG)
            my_print2(self.name, "finished", self.buffer[0].name)
            self.buffer[0].CustomerServingEv.set()
            self.buffer.pop(0)

            if simulation.numCompleted == Customer.count:
                print("thread " + self.name + " terminated " + str(simulation.numCompleted))
                sys.exit() # all Customers finished

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
        #print(str(round(simulation.getCurrentTime())) + ":" + station + " " + status + " customer " + kunde)
        print("%s: %s %s %s" % (str(round(simulation.getCurrentTime())), station, status, kunde))


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
            station = self.getStation()
            if len(station.buffer) < self.getMaxQueueLen():
                station.queue(self)
                my_print1(self.name, "Queueing", station.name)
            else:
                my_print1(self.name, "Dropped", station.name)

            station = self.getStation()
            station.CustomerWaitingEv.set()
            self.CustomerServingEv.wait()
            self.CustomerServingEv.clear()
            # customer gets served
            my_print1(self.name, "Finished", station.name)
            self.ekList.pop(0)
            if len(self.ekList) == 0:
                #print(self.name + " eklist empty")
                break
        # kunde DONE
        #my_print1(self.name, "", " DONE")
        simulation.numCompleted += 1
        print("thread " + self.name + " terminated " + str(simulation.numCompleted))
        sys.exit()

    def getWegzeit(self):
        return self.ekList[0][0]

    def getStation(self):
        return self.ekList[0][1]

    def getAnzahlItems(self):
        return self.ekList[0][2]

    def getMaxQueueLen(self):
        return self.ekList[0][3]

    def printStatus(self, kunde, status, station):
        #print(str(round(simulation.getCurrentTime())) + ":" + kunde + " " + status + " at " + station)
        print("%s: %s %s %s" % (str(round(simulation.getCurrentTime())), kunde, status, station))

class Sim:

    startTime = time.time()
    simDone = False
    DEBUG = 1000
    numCompleted = 0

    def getCurrentTime(self):
        return (time.time() * simulation.DEBUG) - (self.startTime * simulation.DEBUG)


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        kunde.start()
        allCustomers.append(kunde)
        i += 1
        t += dT
        Customer.count += 1

if __name__ == "__main__":

    simulation = Sim()

    baeckerTest = Station(5, "BäckerTest")
    baeckerTest.start()

    baecker = Station(10, "Bäcker")
    baecker.start()
    metzger = Station(30, "Metzger")
    metzger.start()
    kaese = Station(60, "Käse")
    kaese.start()
    kasse = Station(5, "Kasse")
    kasse.start()

    Customer.served["Bäcker"] = 0
    Customer.served["Metzger"] = 0
    Customer.served["Käse"] = 0
    Customer.served["Kasse"] = 0
    Customer.dropped["Bäcker"] = 0
    Customer.dropped["Metzger"] = 0
    Customer.dropped["Käse"] = 0
    Customer.dropped["Kasse"] = 0



    einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
    einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
    startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
    startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)

    ekListTest = [(3, baeckerTest, 2, 10)]
    kundeA1 = Customer(list(einkaufsliste1), "A1", 1)
    #kundeA1.start()
    kundeA2 = Customer(list(ekListTest), "A2", 5)
    # kundeA2.start()

for t in allCustomers:
        t.join()

print("dreck")

f.close()
fc.close()
fs.close()