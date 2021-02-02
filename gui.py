# from flask import Flask, render_template, flash
# from flask_bootstrap import Bootstrap
# from flask_appconfig import AppConfig
# from flask_wtf import Form, RecaptchaField
# from flask_wtf.file import FileField
# from wtforms import TextField, HiddenField, ValidationError, RadioField,\
#     BooleanField, SubmitField, IntegerField, FormField, validators
# from wtforms.validators import Required
#
#
# # straight from the wtforms docs:
# class TelephoneForm(Form):
#     country_code = IntegerField('Country Code', [validators.required()])
#     area_code = IntegerField('Area Code/Exchange', [validators.required()])
#     number = TextField('Number')
#
#
# class ExampleForm(Form):
#     field1 = TextField('First Field', description='This is field one.')
#     field2 = TextField('Second Field', description='This is field two.',
#                        validators=[Required()])
#     hidden_field = HiddenField('You cannot see this', description='Nope')
#     recaptcha = RecaptchaField('A sample recaptcha field')
#     radio_field = RadioField('This is a radio field', choices=[
#         ('head_radio', 'Head radio'),
#         ('radio_76fm', "Radio '76 FM"),
#         ('lips_106', 'Lips 106'),
#         ('wctr', 'WCTR'),
#     ])
#     checkbox_field = BooleanField('This is a checkbox',
#                                   description='Checkboxes can be tricky.')
#
#     # subforms
#     mobile_phone = FormField(TelephoneForm)
#
#     # you can change the label as well
#     office_phone = FormField(TelephoneForm, label='Your office phone')
#
#     ff = FileField('Sample upload')
#
#     submit_button = SubmitField('Submit Form')
#
#
#     def validate_hidden_field(form, field):
#         raise ValidationError('Always wrong')
#
#
# def create_app(configfile=None):
#     app = Flask(__name__)
#     AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
#                                 # highly recommend =)
#                                 # https://github.com/mbr/flask-appconfig
#     Bootstrap(app)
#
#     # in a real app, these should be configured through Flask-Appconfig
#     app.config['SECRET_KEY'] = 'devkey'
#     app.config['RECAPTCHA_PUBLIC_KEY'] = \
#         '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
#
#     @app.route('/', methods=('GET', 'POST'))
#     def index():
#         form = ExampleForm()
#         form.validate_on_submit()  # to get error messages to the browser
#         flash('critical message', 'critical')
#         flash('error message', 'error')
#         flash('warning message', 'warning')
#         flash('info message', 'info')
#         flash('debug message', 'debug')
#         flash('different message', 'different')
#         flash('uncategorized message')
#         return render_template('index.html', form=form)
#
#     return app
#
# if __name__ == '__main__':
#     create_app().run(debug=True)

import tkinter as tk
from PIL import ImageTk, Image
import wx
import time
import serial
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QThread, QThreadPool, Signal
import merger
# will set up GUI later after figure out main data merging

class Team_GUI(QMainWindow):

    def __init__(self, parent = None):
        #self.app = QApplication()
        #self.app.setWindowIcon(QIcon('mouse.PNG'))
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
        logo_label.setPixmap(QPixmap('mouse.png').scaled(300, 300))
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
        #dialog = Merge()
        #self.dialogs.append(dialog)
        #dialog.show()
        self.hide()
        mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
        mg.merge()

    def on_serial_clicked(self):
        self.hide()
        #dialog = SerialHome()
        #self.dialogs.append(dialog)
        #dialog.show()

    def run(self):
        self.app.exec_()


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
        print(self.serial)
        self.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.front()
        self.mouseThread = ScanMouseIdThread(self.serial)
        #self.sig = Signal(str)
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
            time.sleep(2)
            self.hide()
        except:
            pass

class ScanMouseIdThread(QThread):
    sig1 = Signal(str)
    count = 1
    def __init__(self, serial, parent=None):
        super(ScanMouseIdThread, self).__init__(parent)
        self.port = serial

    def run(self):
        self.running = True
        while self.running:
            with serial.Serial(self.port, 9600) as rfid_reader:
                tag = rfid_reader.readline().decode('UTF-8').strip()
                self.sig1.emit(tag)
                time.sleep(1)

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

