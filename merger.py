import pandas as pd
from csv import reader
import numpy as np

class Merger():

    def __init__(self, ci_file_path, rfid_file_path):
        self.ci_fp = ci_file_path
        self.rfid_fp = rfid_file_path
        self.ci = None
        self.rfid = None
        self.merged = None

    def merge(self):
        if self.check_ci_file() == -1:
            return -1
        if self.check_rfid_file() == -1:
            return -1
        self.split_by_cage()
        self.merging()
        self.write_to_file()

    def check_ci_file(self):
        # read the ci file check if exists
        # do some common sense verification
        rowcount = 0
        dataflag = 0
        ci_csv_reader = None
        try:
            ci_csv_reader = reader(open(self.ci_fp, 'r'))
        except:
            print("Invalid file path")
            return -1
        for row in ci_csv_reader:
            if 'Int' in row \
                    and 'Cage' in row \
                    and 'Time' in row \
                    and 'Wheel (counts)' in row\
                    and 'Wheel Accum (counts)' in row:
                dataflag = 1
                break
            rowcount += 1
        if dataflag == 0:
            print("Improper file format")
            return -1
        self.ci = pd.read_csv(self.ci_fp,
                             skiprows=rowcount,
                             usecols=['Int','Cage', 'Time', 'Wheel (counts)', 'Wheel Accum (counts)'],
                             parse_dates=['Time'])
        return 0

    def check_rfid_file(self):
        # read the rfid file check if exists
        try:
            self.rfid = pd.read_csv(self.rfid_fp,
                                   usecols=['Cage', 'Time', 'ID'],
                                   parse_dates=['Time'])
        except:
            print('Invalid file')
            return -1
        return 0

    def split_by_cage(self):
        # split the data into separate dataframes by cage number
        cages = self.ci['Cage'].unique().tolist()
        ci = {}
        rf = {}
        self.merged = {}
        for cage in cages:
            ci[cage] = self.ci.loc[self.ci.Cage == cage]
            rf[cage] = self.rfid.loc[self.rfid.Cage == cage]
            self.merged[cage] = pd.DataFrame(columns=['ID','Start Time', 'End Time', 'Wheel (counts)'])
        self.ci = ci
        self.rfid = rf

    def merging(self):
        # finds start and end time by pairs then get the sum of the ci wheel data within these constraints
        for cage in self.rfid:
            pairs = np.array_split(self.rfid[cage], self.rfid[cage].shape[0]/2)
            for pair in pairs:
                # do an error check here to make sure the IDs are same also ensure the format of columns is good
                id = pair.iloc[0, 2]
                start = pair.iloc[0, 1]
                end = pair.iloc[1, 1]
                mask = (self.ci[cage]['Time']>=start) & (self.ci[cage]['Time']<=end)
                wheelcount = self.ci[cage].loc[mask]['Wheel (counts)'].sum()
                self.merged[cage] = self.merged[cage].append({'ID': id, 'Start Time': start, 'End Time': end, 'Wheel (counts)': wheelcount}, ignore_index=True)

    def write_to_file(self):
        # this function needs to be rewritten so there'll be a single file with multiple sheets
        # with each sheet represents a cage also with the raw data vs calculations julio wants
        for cage in self.merged:
            self.merged[cage].to_csv('Cage'+str(cage)+'.csv', index=False)






