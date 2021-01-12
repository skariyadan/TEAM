import pandas as pd
from csv import reader
import numpy as np
import math
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        return 0

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
            self.merged[cage] = pd.DataFrame(columns=['ID','Start Time', 'End Time', 'Wheel (counts)', 'Total Distance Traveled (km)', 'Velocity (km/hr)'])
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
                distance = wheelcount * (29/8) * math.pi * 0.00000254
                velocity = (distance / (pd.Timedelta(end - start).seconds / 3600.0))
                self.merged[cage] = self.merged[cage].append({'ID': id, 'Start Time': start, 'End Time': end, 'Wheel (counts)': wheelcount, 'Total Distance Traveled (km)': distance, 'Velocity (km/hr)': velocity}, ignore_index=True)

    def cumulative(self, cage):
        by_mouse = pd.DataFrame(columns = ['ID', 'Cumulative Time (hr)', 'Cumulative Wheel (counts)', 'Cumulative Distance Traveled (km)', 'Average Velocity (km/hr)'])
        mice = self.merged[cage]['ID'].unique().tolist()
        for mouse in mice:
            mouse_cage_data = self.merged[cage][self.merged[cage]['ID'] == mouse]
            time = mouse_cage_data["End Time"].sub(mouse_cage_data["Start Time"], fill_value = 0).sum().seconds / 3600.0
            wheelcount = mouse_cage_data['Wheel (counts)'].sum()
            distance = wheelcount * (29/8) * math.pi * 0.00000254
            velocity = (distance / time)
            by_mouse = by_mouse.append({'ID': mouse, 'Cumulative Time (hr)' : time, 'Cumulative Wheel (counts)' : wheelcount, 'Cumulative Distance Traveled (km)' : distance, 'Average Velocity (km/hr)': velocity}, ignore_index = True)
        return by_mouse

    def graph(self, cage):
        mice = self.merged[cage]['ID'].unique().tolist()
        time_points = self.ci[cage]['Time'].tolist()
        fig, ax = plt.subplots()
        ax.set(title = 'Mice Activity in Cage ' + str(cage) + '\nfrom ' + time_points[0].strftime('%m-%d-%Y') + '-' + time_points[-1].strftime("%m-%d-%Y"),
               xlabel = 'Time',
               ylabel = 'Activity Level')
        if (time_points[-1]-time_points[0]).days <= 0:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y\n%H:%M"))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=20))
            ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
            ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=2))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%y"))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=4))
        plt.xticks(rotation=90, fontsize=6)
        plt.setp(ax.xaxis.get_minorticklabels(), rotation=90, fontsize=5)
        ax.set_xlim(time_points[0], time_points[-1])
        for mouse in mice:
            mouse_data = {t : 0 for t in time_points}
            mouse_cage_data = self.merged[cage][self.merged[cage]['ID'] == mouse]
            for idx, row in mouse_cage_data.iterrows():
                start = row['Start Time']
                end = row['End Time']
                mouse_time_intervals = self.ci[cage].loc[(self.ci[cage]['Time']>=start) & (self.ci[cage]['Time']<=end)]
                for mt_idx, mt_row in mouse_time_intervals.iterrows():
                    mouse_data[mt_row["Time"]] = mt_row["Wheel (counts)"]
            plt.plot(time_points, list(mouse_data.values()), label=mouse)
        plt.legend(bbox_to_anchor=(1.1,1.15), loc='upper right', fontsize='xx-small', title="Mice")
        fig.subplots_adjust(right=0.9)
        if len(list(ax.xaxis.get_ticklabels(minor=True))) >= 10:
            [l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels()) if i % 2 != 0 and i != len(ax.xaxis.get_ticklabels()) -1 ]
            [l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels(minor=True)) if i % 2 == 0]
        if len(list(plt.xticks()[0])) > 1:
            diff = (list(plt.xticks()[0])[-1] - list(plt.xticks()[0])[0]) / (len(list(plt.xticks()[0])) - 1)
            plt.xticks(list(plt.xticks()[0]) + [list(plt.xticks()[0])[0] - diff, list(plt.xticks()[0])[-1] + diff])
        plt.savefig("plot.png")

    def write_to_file(self):
        # this function needs to be rewritten so there'll be a single file with multiple sheets
        # with each sheet represents a cage also with the raw data vs calculations julio wants
        writer = pd.ExcelWriter('MouseData.xlsx', engine = 'xlsxwriter')
        workbook = writer.book
        for cage in self.merged:
            worksheet = workbook.add_worksheet('Cage'+ str(cage) + '-Raw')
            writer.sheets['Cage' + str(cage) + '-Raw'] = worksheet
            worksheet.write_string(0,0, 'Cage'+ str(cage) + " Raw Data")
            self.merged[cage].to_excel(writer, sheet_name='Cage'+ str(cage) + '-Raw', startrow=1, startcol=0, index=False)
            worksheet = workbook.add_worksheet('Cage' + str(cage) + '-Calculations')
            writer.sheets['Cage' + str(cage) + '-Calculations'] = worksheet
            worksheet.write_string(0, 0, 'Cage' + str(cage) + " Data (With Calculations)")
            self.merged[cage].to_excel(writer, sheet_name='Cage' + str(cage) + '-Calculations', startrow=1, startcol=0, index=False)
            worksheet.write_string(self.merged[cage].shape[0] + 4, 0, "Cumulative Data")
            self.cumulative(cage).to_excel(writer, sheet_name='Cage' + str(cage) + '-Calculations', startrow=self.merged[cage].shape[0] + 5, startcol=0, index=False)
            self.graph(cage)
            worksheet.insert_image(0, self.merged[cage].shape[1] + 5, "plot.png")
        writer.save()






