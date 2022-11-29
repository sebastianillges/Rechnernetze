import os
import re
import matplotlib.pyplot as plt

regexSize = "(?<=mit )([0-9]*)(?= Bytes)"
regexTimes = "(?<=Mittelwert = )([0-9]*)(?=ms)"

pagackeSizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
#pagackeSizes = [1, 2]
os.remove("pingFiles/pingBySizeHTWG.txt")
for s in pagackeSizes:
    os.system("ping www.htwg-konstanz.de -l " + str(s) + " >> pingFiles/pingBySizeHTWG.txt")

resultsSize = []
resultsTime = []

output = open("pingFiles/pingBySizeHTWG.txt", errors="ignore").readlines()
for s in output:
    matchSize = re.search(regexSize, s)
    matchTime = re.search(regexTimes, s)
    if matchSize is not None:
        resultsSize.append(float(matchSize[1]))
    if matchTime is not None:
        resultsTime.append(float(matchTime[1]))

print(resultsSize)
print(resultsTime)

plt.plot(resultsSize, resultsTime, label="HTWG")
plt.xlabel("package size in Bytes")
plt.ylabel("response time in ms")
plt.legend(loc="best")
plt.savefig("plotbysize.png", dpi=500)
plt.show()