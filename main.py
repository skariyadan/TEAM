import tkinter as tk
import gui
import merger
import wx

def main():
    # app = gui.Team_GUI()
    # app.run()
    mg = merger.Merger('resources/SreeSampleData.csv', 'resources/SreeRFIDData.csv')
    mg.merge()


if __name__ == "__main__":
    main()


