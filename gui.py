import tkinter as tk
from PIL import ImageTk, Image
import wx
import time
import serial
import pandas as pd
from datetime import datetime
import traceback
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QThread, QThreadPool, Signal
import merger

class Team_GUI(QMainWindow):

    def __init__(self, parent = None):
        super(Team_GUI, self).__init__(parent)
        self.dialogs = list()
        self.front()


    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

        grid = QGridLayout()

        logo_title = QLabel("TEAM", self)
        font = QFont('Arial', 100)
        font.setBold(True)
        logo_title.setStyleSheet("QLabel {color: #fcba03}")
        logo_title.setFont(font)
        grid.addWidget(logo_title, 0, 1)

        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap('mouse.png').scaled(400, 400))
        grid.addWidget(logo_label, 1, 1)

        self.input_button = QPushButton("Serial Input", self)
        self.input_button.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.input_button.clicked.connect(lambda: self.on_serial_clicked())
        grid.addWidget(self.input_button, 2, 0, 1, 1)

        self.merge_button = QPushButton("Merge Data", self)
        self.merge_button.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.merge_button.clicked.connect(lambda: self.on_merge_clicked())
        grid.addWidget(self.merge_button, 2,2, 1, 1)

        central = QWidget()
        central.setLayout(grid)
        self.setCentralWidget(central)


    def on_merge_clicked(self):
        self.hide()
        mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
        mg.merge()

    def on_serial_clicked(self):
        self.hide()



class MergeHome(QMainWindow):

    def __init__(self, parent=None):
        super(MergeHome, self).__init__(parent)
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.front()

    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

class SerialHome(QMainWindow):
    def __init__(self, parent=None):
        super(SerialHome, self).__init__(parent)
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.front()

    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

        grid = QGridLayout()

        logo_title = QLabel("Serial Input", self)
        font = QFont('Arial', 30)
        font.setBold(True)
        logo_title.setStyleSheet("QLabel {color: #fcba03}")
        logo_title.setFont(font)
        logo_title.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_title, 0, 1)

        logo_instr = logo_title = QLabel("Enter serial port to read tags from:", self)
        font = QFont('Arial', 15)
        font.setBold(True)
        logo_instr.setStyleSheet("QLabel {color: #fcba03}")
        logo_instr.setFont(font)
        logo_instr.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_instr, 1, 1)

        self.serial = QLineEdit()
        font = QFont('Arial', 15)
        self.serial.setFont(font)
        #self.serial.setAlignment(Qt.AlignTop)
        self.serial.setStyleSheet("QLineEdit {background: #ffffff}")
        grid.addWidget(self.serial, 2, 1)
        grid.setAlignment(self.serial, Qt.AlignTop)

        self.back = QPushButton("Back", self)
        self.back.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.back.clicked.connect(self.hide)
        grid.addWidget(self.back, 3, 0, 1, 1)

        self.start = QPushButton("Start", self)
        self.start.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.start.clicked.connect(self.hide)
        self.start.setDisabled(True)
        self.serial.textChanged.connect(self.disableStartButton)
        grid.addWidget(self.start, 3, 2, 1, 1)

        central = QWidget()
        central.setLayout(grid)
        self.setCentralWidget(central)

    def disableStartButton(self):
        if len(self.serial.text()) > 0:
            self.start.setDisabled(False)

class SerialScan(QMainWindow):

    def __init__(self, serial, parent=None):
        super(SerialScan, self).__init__(parent)
        self.serial = serial
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.IdToName = {}
        self.front()
        self.mouseThread = ScanMouseIdThread(self.serial)
        self.mouseThread.start()
        self.mouseThread.sig1.connect(self.on_info)

    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

        grid = QGridLayout()

        logo_title = QLabel("Serial Input: Scan IDs", self)
        font = QFont('Arial', 30)
        font.setBold(True)
        logo_title.setStyleSheet("QLabel {color: #fcba03}")
        logo_title.setFont(font)
        logo_title.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_title, 0, 1)

        logo_instr = logo_title = QLabel("Scan mouse tags, enter what cage they are for, and their name:", self)
        font = QFont('Arial', 15)
        font.setBold(True)
        logo_instr.setStyleSheet("QLabel {color: #fcba03}")
        logo_instr.setFont(font)
        logo_instr.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_instr, 1, 1)


        self.miceTable = QTableWidget()
        self.miceTable.setStyleSheet("QTableWidget {background: #ffffff}")
        self.miceTable.setRowCount(1)
        self.miceTable.setColumnCount(3)
        self.miceTable.setHorizontalHeaderLabels(["Mouse Tag", "Cage", "Mouse Name"])
        header = self.miceTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.miceTable.move(0, 0)
        grid.addWidget(self.miceTable, 2, 1)

        '''
        self.add = QPushButton("Add Mouse Row", self)
        self.add.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.add.clicked.connect(lambda: self.addRow())
        grid.addWidget(self.add, 3, 1, 1, 1)
        '''

        self.back = QPushButton("Back", self)
        self.back.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.back.clicked.connect(self.stopThread)
        grid.addWidget(self.back, 4, 0, 1, 1)

        self.start = QPushButton("Start", self)
        self.start.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.start.clicked.connect(self.stopThread)
        grid.addWidget(self.start, 4, 2, 1, 1)

        central = QWidget()
        central.setLayout(grid)
        self.setCentralWidget(central)

    def addRow(self):
        rowPos = self.miceTable.rowCount()
        self.miceTable.insertRow(rowPos)

    def on_info(self, info):
        rowPos = self.miceTable.rowCount() - 1
        item = QTableWidgetItem(info)
        self.miceTable.setItem(rowPos, 0, item)
        self.miceTable.insertRow(rowPos+1)

    def stopThread(self):
        try:
            self.mouseThread.running = False
            time.sleep(3)
            #self.mouseThread.terminate()
            #time.sleep(3)
            self.miceTable.clearSelection()
            for row in range(self.miceTable.rowCount()):
                if self.miceTable.item(row, 0) and self.miceTable.item(row, 1) and self.miceTable.item(row, 2):
                    mouseId = self.miceTable.item(row, 0).text().strip()
                    cage = int(self.miceTable.item(row, 1).text().strip())
                    name = self.miceTable.item(row, 2).text().strip()
                    self.IdToName[mouseId] = [cage, name]
            self.mouseThread.serial_port.close()
            self.hide()
        except:
            traceback.print_exc()

class ScanMouseIdThread(QThread):
    sig1 = Signal(str)
    def __init__(self, ser, parent=None):
        super(ScanMouseIdThread, self).__init__(parent)
        self.port = ser
        self.serial_port = serial.Serial(self.port, 9600)

    def run(self):
        self.running = True
        while self.running:
            with self.serial_port as rfid_reader:
                tag = rfid_reader.readline().decode('UTF-8').strip()
                self.sig1.emit(tag)
                time.sleep(1)



class SerialExperiment(QMainWindow):
    def __init__(self, IdToName, serial, parent=None):
        super(SerialExperiment, self).__init__(parent)
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.IdToName = IdToName
        self.serial = serial
        self.RFIDData = pd.DataFrame(columns=["Cage", "Time", "ID"])
        self.mouseThread = ScanMouseIdThread(self.serial)
        self.mouseThread.start()
        self.mouseThread.sig1.connect(self.on_info)
        self.front()

    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

        grid = QGridLayout()

        logo_title = QLabel("Serial Input", self)
        font = QFont('Arial', 30)
        font.setBold(True)
        logo_title.setStyleSheet("QLabel {color: #fcba03}")
        logo_title.setFont(font)
        logo_title.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_title, 0, 1)

        logo_instr = logo_title = QLabel("Experiment In Progress", self)
        font = QFont('Arial', 30)
        font.setBold(True)
        logo_instr.setStyleSheet("QLabel {color: #fcba03}")
        logo_instr.setFont(font)
        logo_instr.setAlignment(Qt.AlignCenter)
        grid.addWidget(logo_instr, 1, 1)

        self.back = QPushButton("Back", self)
        self.back.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.back.clicked.connect(self.hide)
        grid.addWidget(self.back, 4, 0, 1, 1)

        self.start = QPushButton("Done", self)
        self.start.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        self.start.clicked.connect(self.stopThread)
        grid.addWidget(self.start, 4, 2, 1, 1)

        central = QWidget()
        central.setLayout(grid)
        self.setCentralWidget(central)

    def on_info(self, info):
        id = info
        time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        cage = self.IdToName[id][0]
        self.RFIDData = self.RFIDData.append({"Cage": cage, "Time": time, "ID": self.IdToName[id][1]},
                                             ignore_index=True)

    def stopThread(self):
        try:
            self.mouseThread.running = False
            time.sleep(2)
            print(self.RFIDData)
            self.hide()
        except:
            pass

class Manager:
    def __init__(self):
        self.home = Team_GUI()
        self.serial_home = SerialHome()
        self.merge_home = MergeHome()

        self.home.input_button.clicked.connect(self.serial_home.show)
        self.serial_home.back.clicked.connect(self.home.show)
        self.home.merge_button.clicked.connect(self.merge_home.show)
        self.serial_home.start.clicked.connect(lambda: self.serialscaninit())


        self.home.show()

    def serialscaninit(self):
        self.serial_scan = SerialScan(self.serial_home.serial.text())
        self.serial_scan.show()
        self.serial_scan.back.clicked.connect(self.serial_home.show)
        self.serial_scan.start.clicked.connect(lambda: self.serialexperimentinit())

    def serialexperimentinit(self):
        if not self.serial_scan.isVisible():
            self.serial_experiment = SerialExperiment(self.serial_scan.IdToName, self.serial_scan.serial)
            self.serial_experiment.show()
            self.serial_experiment.back.clicked.connect(self.serial_home.show)





