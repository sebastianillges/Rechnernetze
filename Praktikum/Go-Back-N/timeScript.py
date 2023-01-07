import csv
import os

try:
    os.remove("results.csv")
except:
    pass

header = ["Window Size", "Time"]
csvFile = open("results.csv", "a", encoding="UTF8", newline='')
writer = csv.writer(csvFile)
writer.writerow(header)
csvFile.close()

for i in range(1, 18):
    os.system(".\GobackNSocket.py " + str(2**i))