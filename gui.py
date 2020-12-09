import tkinter as tk
from PIL import ImageTk, Image
import wx

# will set up GUI later after figure out main data merging

class Team_GUI(wx.App):

    def __init__(self):
        super().__init__()
        self.root = wx.Frame(parent=None, title="TEAM")
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("resources/mouse.ico", wx.BITMAP_TYPE_ANY))
        self.root.SetIcon(icon)
        self.root.Set
        self.root.Show()




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