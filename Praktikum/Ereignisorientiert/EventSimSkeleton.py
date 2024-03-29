import os
import sys
import heapq

f = open(os.path.join(sys.path[0], "supermarkt.txt"), "w")
fc = open(os.path.join(sys.path[0], "supermarkt_customer.txt"), "w")
fs = open(os.path.join(sys.path[0], "supermarkt_station.txt"), "w")


# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, stat, msg):
    t = EvQueue.time
    print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + stat)
    fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + stat + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(stat, msg, name):
    t = EvQueue.time
    print(str(round(t, 4)) + ':' + stat + ' ' + msg)
    fs.write(str(round(t, 4)) + ':' + stat + ' ' + msg + ' ' + name + '\n')


# class consists of instance variables:
# t: time stamp
# work: job to be done
# args: list of arguments for job to be done
# prio: used to give leaving, being served, and arrival different priorities
class Ev:
    counter = 0

    def __init__(self, t, work, args=(), prio=255):
        self.t = t
        self.n = Ev.counter
        self.work = work
        self.args = args
        self.prio = prio
        Ev.counter += 1

    def __lt__(self, other):
        if self.t < other.t:
            return True
        elif self.t == other.t:
            return self.prio < other.prio
        else:
            return False

    def __le__(self, other):
        if self.t < other.t:
            return True
        elif self.t == other.t:
            return self.prio <= other.prio
        else:
            return False


# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EvQueue:
    # please implement here
    q = []

    time = 0
    evCount = 0

    def __init__(self):
        heapq.heapify(self.q)

    def push(self, ev):
        heapq.heappush(self.q, ev)

    def pop(self):
        return heapq.heappop(self.q)

    def start(self):
        while EvQueue.q.__len__() > 0:
            ev = EvQueue.pop(self)
            EvQueue.time = ev.t

            evN = ev.work()
            if type(evN) is list:
                if evN.__len__() == 1:
                    self.push(evN.pop(0))
                else:
                    self.push(evN.pop(0))
                    self.push(evN.pop(0))
            elif evN is not None:
                self.push(evN)


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station:
    # please implement here
    def __init__(self, d, n):
        self.delay_per_item = d
        self.name = n
        self.buffer = []
        self.CustomerWaiting = False
        self.busy = False

    def queue(self, kunde):
        self.buffer.append(kunde)
        self.CustomerWaiting = True
        my_print1(kunde.name, self.name, " Queueing at ")
        my_print2(self.name, "Adding Customer", kunde.name)

    def bedienen(self):
        kunde = self.buffer.pop(0)
        my_print2(self.name, " Finished Customer", kunde.name)
        self.busy = True
        if self.buffer.__len__() == 0:
            self.CustomerWaiting = False
        Customer.served[self.name] += 1
        return kunde

    def isBusy(self):
        return self.busy

    def kundeWartet(self):
        return self.CustomerWaiting


# class consists of
# statistics variables
# and methods as described in the problem description
class Customer:
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    # please implement here

    def __init__(self, ekList, name, startTime):
        self.ekList = ekList
        self.name = name
        self.startTime = startTime
        Customer.count += 1
        self.flag = 0

    def run(self):
        t = self.ekList[0][0]
        station = self.ekList[0][1]
        ev = Ev(EvQueue.time + t, self.ankunft, prio=3, args=(str(station), self.name))
        return ev

    def ankunft(self):
        t = self.ekList[0][1].delay_per_item * self.ekList[0][2]
        station = self.ekList[0][1]
        if station.isBusy() is False and station.kundeWartet() is False:
            station.queue(self)
            my_print2(station.name, " Serving customer ", self.name)
            station.busy = True
            ev = Ev(EvQueue.time + t, self.verlassen, prio=1, args=(str(station), self.name))
            return ev
        elif self.ekList[0][3] < len(station.buffer):
            my_print1(self.name, station.name, " Dropped at ")
            Customer.dropped[station.name] += 1
            self.flag = 1
            my_print1(self.name, station.name, " Queueing at ")
            self.ekList.pop(0)
            t = self.ekList[0][0]
            ev = Ev(EvQueue.time + t, self.ankunft, prio=3, args=(str(station), self.name))
            return ev
        else:
            station.queue(self)
            ev = None
            return ev

    def verlassen(self):
        station = self.ekList[0][1]
        kundeAlt = station.bedienen()
        station.busy = False
        my_print1(self.name, station.name, " Finished at ")
        if kundeAlt.name != self.name or kundeAlt.startTime != self.startTime:
            print("The wrong Costumer was served")
        self.ekList.pop(0)
        if self.ekList.__len__() > 0:
            t = self.ekList[0][0]
            ev = [Ev(EvQueue.time + t, self.ankunft, prio=3, args=(str(station), self.name))]
        else:
            Customer.duration += EvQueue.time - self.startTime
            if self.flag == 0:
                Customer.complete += 1
                Customer.duration_cond_complete += EvQueue.time - self.startTime

            ev = None

        if station.CustomerWaiting:
            kunde = station.buffer[0]
            t = kunde.ekList[0][1].delay_per_item * kunde.ekList[0][2]
            if ev is None:
                ev = (Ev(EvQueue.time + t, kunde.verlassen, prio=1, args=(str(station), kunde.name)))
            else:
                ev.append(Ev(EvQueue.time + t, kunde.verlassen, prio=1, args=(str(station), kunde.name)))
        return ev


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        ev = Ev(t, kunde.run, prio=2)
        evQ.push(ev)
        i += 1
        t += dT


evQ = EvQueue()
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
evQ.start()
my_print('Simulationsende: %is' % EvQueue.time)
my_print('Anzahl Kunden: %i' % Customer.count)
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
