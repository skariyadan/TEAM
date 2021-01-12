import argparse
import serial #pip3 install pyserial
import pandas as pd #pip3 install pandas
from datetime import datetime

class Parser():

    def __init__(self):
        self.port = input('Enter serial port to read tags from: ')
        self.IDToName = {}
        self.RFIDData = pd.DataFrame(columns=["Cage", "Time", "ID"])
        self.mouseCount = 1

    def readTagsInitially(self):
        print("Scan mouse tags, hit Ctrl-C when you're done")
        while True:
            try:
                with serial.Serial(self.port, 9600) as rfid_reader:
                    tag = rfid_reader.readline().decode('UTF-8').strip()
                    print(tag)
                    cage = input("Enter what number cage this mouse is for (numerical only): ")
                    self.IDToName[tag] = [int(cage), "Mouse" + str(self.mouseCount)]
                    self.mouseCount += 1
                    print(tag)
            except KeyboardInterrupt:
                return


    def scanId(self):
        print("Begin experiment, hit Ctrl-C when you're done")
        while True:
            try:
                with serial.Serial(self.port, 9600) as rfid_reader:
                    id = rfid_reader.readline().decode('UTF-8').strip()
                    time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    cage = self.IDToName[id][0]
                    self.RFIDData = self.RFIDData.append({"Cage": cage, "Time":time, "ID": self.IDToName[id][1]}, ignore_index=True)
                    print(cage, time, id)
            except KeyboardInterrupt:
                return


    def run(self):
        self.readTagsInitially()
        self.scanId()
        self.RFIDData.to_csv('RFIDData.csv', index=False)
        print(self.RFIDData)
        print("Data saved to file RFIDData.csv")



'''
    def __init__(self, port):
        self.port = port
        self.IDToName = {}
        self.RFIDData = pd.DataFrame(columns=["Cage", "Time", "ID"])
        self.mouseCount = 1

    def readAndMap(self):
        mouse = None
        with serial.Serial(self.port, 9600) as rfid_reader:
            while (mouse is None):
                mouse = rfid_reader.readline().decode('UTF-8').strip()
                self.IDToName[mouse] = "Mouse" + str(self.mouseCount)
                self.mouseCount += 1

'''
