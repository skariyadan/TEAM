import tkinter as tk
from PIL import ImageTk, Image
import wx
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from PySide6.QtGui import QIcon, QPixmap
# will set up GUI later after figure out main data merging

class Team_GUI():

    def __init__(self):
        self.app = QApplication()
        self.app.setWindowIcon(QIcon('resources/mouse.PNG'))
        self.main = self.front()
        self.main.show()


    def front(self):
        window = QMainWindow()
        window.setGeometry(500, 500, 500, 500)
        window.setWindowTitle("TEAM")
        window.setWindowIcon(QIcon('resources/mouse.PNG'))
        window.setStyleSheet("background-color: #03795E")
        grid = QGridLayout()
        logo_label = QLabel(window)
        logo_label.setPixmap(QPixmap('resources/mouse').scaled(700,700))
        grid.addWidget(logo_label, 1, 1)

        central = QWidget()
        central.setLayout(grid)
        window.setCentralWidget(central)
        return window

    def run(self):
        self.app.exec_()





'''
class MyApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TEAM")
        self.root.geometry("600x600")
        #root.iconphoto(False, tk.PhotoImage(file='resources/mouse.jpg'))
        root.configure(background='#bce6eb')
        img = ImageTk.PhotoImage(Image.open("resources/mouse.jpg"))
        label = tk.Label(root, image=img)
        label.pack(fill=tk.BOTH, expand=tk.YES)
        label.bind('<Configure>', resize_image)
        root.mainloop()

    def resize_image(label, event):
        new_width = event.width
        new_height = event.height

        label = label.resize((new_width, new_height))

        label = ImageTk.PhotoImage(label)
        label.configure(image= img)
'''