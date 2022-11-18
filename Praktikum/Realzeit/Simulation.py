import os.path
import sys
import time
from threading import Thread, Lock, Event

f = open(os.path.join(sys.path[0], "supermarkt.txt"), "w")
fc = open(os.path.join(sys.path[0], "supermarkt_customer.txt"), "w")
fs = open(os.path.join(sys.path[0], "supermarkt_station.txt"), "w")

allCustomers = []
allStations = []

# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print_k(k, s, msg):
    t = simulation.getCurrentTime()
    print(str(round(t / 1000000000)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t / 1000000000)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print_s(s, msg, name):
    t = simulation.getCurrentTime()
    print(str(round(t / 1000000000))+':'+s+' '+msg)
    fs.write(str(round(t / 1000000000)) + ':' + s + ' ' + msg + ' ' + name + '\n')

class Station(Thread):
    def __init__(self, d, n):
        super().__init__()
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.busy = False
        self.CustomerWaitingEv = Event()
        self.bufferLock = Lock()
        self.eventLock = Lock()

    def run(self):
        allStations.append(self)
        while 1:

            if len(self.buffer) != 0:
                self.setCustomerWaitingEv()

            self.CustomerWaitingEv.wait()
            if len(allCustomers) == 0:
                #print("thread " + self.name + " terminated")
                sys.exit()  # all Customers finished
            # kunde angekommen
            self.clearCustomerWaitingEv()

            my_print_s(self.name, "adding", self.buffer[0].name)
            my_print_s(self.name, "serving", self.buffer[0].name)
            time.sleep((self.buffer[0].getAnzahlItems() * self.delay_per_item) / simulation.DEBUG)
            my_print_s(self.name, "finished", self.buffer[0].name)

            self.buffer[0].CustomerServingEv.set()

            self.buffer.pop(0)


    def setCustomerWaitingEv(self):
        self.eventLock.acquire()
        self.CustomerWaitingEv.set()
        self.eventLock.release()
    def clearCustomerWaitingEv(self):
        self.eventLock.acquire()
        self.CustomerWaitingEv.clear()
        self.eventLock.release()

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
        print("%s: %s %s %s" % (str(simulation.getCurrentTime()), station, status, kunde))


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
        self.droppedFlag = False
        self.endTime = 0
    def run(self):
        allCustomers.append(self)

        time.sleep(self.startTime / simulation.DEBUG)
        while 1:
            if len(self.ekList) == 0:
                break
            # walking to station
            time.sleep(self.getWegzeit() / simulation.DEBUG)
            # customer arrived
            station = self.getStation()
            station.CustomerWaitingEv.set()
            if len(station.buffer) <= self.getMaxQueueLen():
                station.queue(self)
                my_print_k(self.name, station.name, "Queueing")

                self.CustomerServingEv.wait()

                self.CustomerServingEv.clear()

                # customer gets served
                my_print_k(self.name, station.name, "Finished")
                self.served[station.name] += 1
            else:
                my_print_k(self.name, station.name, "Dropped")
                self.dropped[station.name] += 1
                self.droppedFlag = True

            self.ekList.pop(0)
        self.endTime = simulation.getCurrentTime() / 1000000000
        # kunde DONE
        #my_print_k(self.name, "", " DONE")
        if len(allCustomers) == 1:
            simulation.endTime = simulation.getCurrentTime()
            for s in allStations:
                s.CustomerWaitingEv.set()
        allCustomers.remove(self)
        Customer.duration += (self.endTime - self.startTime)
        if self.droppedFlag is False:
            Customer.complete += 1
            Customer.duration_cond_complete += (self.endTime - self.startTime)
        #print("thread " + self.name + " terminated")
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
        print(str(simulation.getCurrentTime()) + ":" + kunde + " " + status + " at " + station)
class Sim:

    startTime = time.time_ns()
    simDone = False
    DEBUG = 1
    maxTime = 3000
    endTime = 0

    def getCurrentTime(self):
        return time.time_ns() - self.startTime

    def setEndTime(self):
        self.endTime = self.getCurrentTime()

def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        kunde.start()
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
    kundeA1 = Customer(list(ekListTest), "A1", 1)
    #kundeA1.start()
    kundeA2 = Customer(list(ekListTest), "A2", 5)
    #kundeA2.start()

for c in allCustomers:
    c.join()
for s in allStations:
    s.join()

my_print('Simulationsende: %is' % simulation.endTime)
my_print('Anzahl Kunden: %i' % (Customer.count))
my_print('Anzahl vollständige Einkäufe %i' % Customer.complete)
x = Customer.duration / Customer.count
my_print(str('Mittlere Einkaufsdauer %.2fs' % x))
x = Customer.duration_cond_complete / Customer.complete
my_print('Mittlere Einkaufsdauer (vollständig): %.2fs' % x)
S = ('Bäcker', 'Metzger', 'Käse', 'Kasse')
for s in S:
    x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
    my_print('Drop percentage at %s: %.2f' % (s, x))

f.close()
fc.close()
fs.close()