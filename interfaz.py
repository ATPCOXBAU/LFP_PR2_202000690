from tkinter import *


class Interface:

    def __init__(self):
        root = Tk()
        root.geometry('850x625')
        root.title('Proyecto 2')
        root.resizable(0, 0)
        self.Frame = Frame(root, width='850', height='625')
        self.Frame.pack()
        self.Frame.config(bg='#EEE8AA')
        root.mainloop()