import tkinter as tk
import gui
import merger
import rfid
import wx

def main():
    serialinput = rfid.Parser()
    serialinput.run()
    '''
    app = gui.Team_GUI()
    app.run()
    mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
    mg.merge()
    '''

if __name__ == "__main__":
    main()


