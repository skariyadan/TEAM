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
        print("Scan Tags hit Ctrl-C when you're done")
        try:
            with serial.Serial(self.port, 9600) as rfid_reader:
                while True:
                    tag = rfid_reader.readline().decode('UTF-8').strip()
                    self.IDToName[tag] = "Mouse" + str(self.mouseCount)
                    self.mouseCount += 1
                    print(tag)
        except KeyboardInterrupt:
            pass

    def scanId(self):
        print("Scan Tags hit Ctrl-C when you're done")
        try:
            with serial.Serial(self.port, 9600) as rfid_reader:
                while True:
                    id = rfid_reader.readline().decode('UTF-8').strip()
                    time = datetime.now().strftime("%H:%M:%S")
                    cage = 1 # lol
                    self.RFIDData = self.RFIDData.append({"Cage": cage, "Time":time, "ID": id}, ignoreIndex=True)
                    print(cage, time, id)
        except KeyboardInterrupt:
            pass

    def run(self):
        self.readTagsInitially()
        self.scanId()
        print(self.RFIDData)



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
