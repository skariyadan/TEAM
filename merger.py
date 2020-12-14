import pandas as pd
from csv import reader
import numpy as np
import math
import xlsxwriter

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
            self.merged[cage] = pd.DataFrame(columns=['ID','Start Time', 'End Time', 'Wheel (counts)', 'Total Distance Traveled (ft)', 'Velocity (ft/hr)'])
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
                distance = wheelcount * (29/8) * math.pi
                velocity = distance / (pd.Timedelta(end - start).seconds / 3600.0)
                self.merged[cage] = self.merged[cage].append({'ID': id, 'Start Time': start, 'End Time': end, 'Wheel (counts)': wheelcount, 'Total Distance Traveled (ft)': distance, 'Velocity (ft/hr)': velocity}, ignore_index=True)

    def cumulative(self, cage_data):
        by_mouse = pd.DataFrame(columns = ['ID', 'Cumulative Time (hr)', 'Cumulative Wheel (counts)', 'Cumulative Distance Traveled (ft)', 'Average Velocity (ft/hr)'])
        mice = cage_data['ID'].unique().tolist()
        for mouse in mice:
            mouse_cage_data = cage_data[cage_data['ID'] == mouse]
            time = (mouse_cage_data["End Time"].sub(mouse_cage_data["Start Time"], fill_value = 0).sum().seconds) / 3600.0
            wheelcount = mouse_cage_data['Wheel (counts)'].sum()
            distance = wheelcount * (29/8) * math.pi
            velocity = distance / time
            by_mouse = by_mouse.append({'ID': mouse, 'Cumulative Time (hr)' : time, 'Cumulative Wheel (counts)' : wheelcount, 'Cumulative Distance Traveled (ft)' : distance, 'Average Velocity (ft/hr)': velocity}, ignore_index = True)
        return by_mouse

    def write_to_file(self):
        # this function needs to be rewritten so there'll be a single file with multiple sheets
        # with each sheet represents a cage also with the raw data vs calculations julio wants
        writer = pd.ExcelWriter('MouseData.xlsx', engine = 'xlsxwriter')
        workbook = writer.book
        for cage in self.merged:
            worksheet = workbook.add_worksheet('Cage'+ str(cage) + '-Raw')
            writer.sheets['Cage'+ str(cage) + '-Raw'] = worksheet
            worksheet.write_string(0,0, 'Cage'+ str(cage) + " Raw Data")
            self.merged[cage].to_excel(writer, sheet_name='Cage'+ str(cage) + '-Raw', startrow=1, startcol=0, index=False)
            worksheet = workbook.add_worksheet('Cage' + str(cage) + '-Calculations')
            writer.sheets['Cage' + str(cage) + '-Calculations'] = worksheet
            worksheet.write_string(0, 0, 'Cage' + str(cage) + " Data (With Calculations)")
            self.merged[cage].to_excel(writer, sheet_name='Cage' + str(cage) + '-Calculations', startrow=1, startcol=0, index=False)
            worksheet.write_string(self.merged[cage].shape[0] + 4, 0, "Cumulative Data")
            self.cumulative(self.merged[cage]).to_excel(writer, sheet_name='Cage' + str(cage) + '-Calculations', startrow=self.merged[cage].shape[0] + 5, startcol=0, index=False)
        writer.save()





