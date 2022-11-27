import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join
from scipy.interpolate import make_interp_spline

# txt files created with: ping url -n 100 >> path to file
pingfiles = [f for f in listdir("pingFiles/") if isfile(join("pingFiles/", f))]
timesNsa = np.loadtxt("pingFiles/pingResultsNsa.txt", dtype=str, usecols=3)
timesHTWG = np.loadtxt("pingFiles/pingResultsHTWG.txt", dtype=str, usecols=3)
timesStackoverflow = np.loadtxt("pingFiles/pingResultsStackoverflow.txt", dtype=str, usecols=4)
timesSydney = np.loadtxt("pingFiles/pingResultsSydney.txt", dtype=str, usecols=3)

for i in range(100):
    timesHTWG[i] = timesHTWG[i][5:7]
    timesNsa[i] = timesNsa[i][5:7]
    timesStackoverflow[i] = timesStackoverflow[i][5:7]
    timesSydney[i] = timesSydney[i][5:7]

timesHTWG = list(map(float, timesHTWG))
timesNsa = list(map(float, timesNsa))
timesStackoverflow = list(map(float, timesStackoverflow))
timesSydney = list(map(float, timesSydney))

plt.plot(timesHTWG, label="HTWG IPv6", linewidth=0.7)
plt.plot(timesNsa, label="NSA IPv6", linewidth=0.7)
plt.plot(timesStackoverflow, label="Stackoverflow IPv4", linewidth=0.7)
plt.plot(timesSydney, label="Sydney IPv6", linewidth=0.7)
plt.xlabel("pings")
plt.ylabel("response time in ms")
plt.legend(loc="best")
plt.savefig("plot.png", dpi=500)
plt.show()
