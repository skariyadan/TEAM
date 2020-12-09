import tkinter as tk
import gui
import merger
import wx

def main():
    pass
    # app = gui.Team_GUI()
    # app.MainLoop()
    mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
    mg.merge()


if __name__ == "__main__":
    main()


