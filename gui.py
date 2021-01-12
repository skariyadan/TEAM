import tkinter as tk
from PIL import ImageTk, Image
import wx
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
import merger
# will set up GUI later after figure out main data merging

class Team_GUI():

    def __init__(self):
        self.app = QApplication()
        self.app.setWindowIcon(QIcon('mouse.PNG'))
        self.dialogs = list()
        self.main = self.front()
        self.main.show()


    def front(self):
        window = QMainWindow()
        window.setGeometry(500, 500, 500, 500)
        window.setWindowTitle("TEAM")
        window.setWindowIcon(QIcon('mouse.PNG'))
        window.setStyleSheet("background-color: #03795E")

        grid = QGridLayout()
        logo_title = QLabel("TEAM", window)
        font = QFont('Arial', 100)
        font.setBold(True)
        logo_title.setStyleSheet("QLabel {color: #fcba03}")
        logo_title.setFont(font)
        grid.addWidget(logo_title, 0, 1)
        logo_label = QLabel(window)
        logo_label.setPixmap(QPixmap('mouse.png').scaled(300, 300))
        grid.addWidget(logo_label, 1, 1)
        input_button = QPushButton("Serial Input", window)
        input_button.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")
        input_button.clicked.connect(lambda: self.on_serial_clicked())
        grid.addWidget(input_button, 2, 0, 1, 1)
        merge_button = QPushButton("Merge Data", window)
        merge_button.setStyleSheet("QPushButton:hover:!pressed{ background: #fcba03}")

        dialogs = list()
        merge_button.clicked.connect(lambda: self.on_merge_clicked())
        grid.addWidget(merge_button, 2,2, 1, 1)


        central = QWidget()
        central.setLayout(grid)
        window.setCentralWidget(central)
        return window

    def on_merge_clicked(self):
        dialog = Merge()
        self.dialogs.append(dialog)
        dialog.show()
        mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
        mg.merge()

    def on_serial_clicked(self):
        dialog = Serial()
        self.dialogs.append(dialog)
        dialog.show()

    def run(self):
        self.app.exec_()


class Merge(QMainWindow):

    def __init__(self, parent=None):
        super(Merge, self).__init__(parent)
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.front()

    def front(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle("TEAM")
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.setStyleSheet("background-color: #03795E")

class Serial(QMainWindow):
    def __init__(self, parent=None):
        super(Serial, self).__init__(parent)
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
        logo_title.setAlignment(Qt.AlignLeft)
        grid.addWidget(logo_title, 0, 1)
        '''
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap('mouse.png').scaled(50, 50))
        grid.addWidget(logo_label, 0, 0)
        '''


        central = QWidget()
        central.setLayout(grid)
        self.setCentralWidget(central)