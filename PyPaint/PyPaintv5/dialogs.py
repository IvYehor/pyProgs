from tkinter import *
from tkinter.colorchooser import askcolor
import numpy as np
from PIL import Image
import math
import random

class SizeChooserDialog:
    def __init__(self, parent, getfunction):
        self.top = Toplevel(parent)
        l1 = Label(self.top, text = "New width")
        self.ew = Entry(self.top)
        l2 = Label(self.top, text = "New width")
        self.eh = Entry(self.top)
        ok_button = Button(self.top, text = "OK", command = lambda: getfunction(self))
        l1.pack()
        self.ew.pack()
        l2.pack()
        self.eh.pack()
        ok_button.pack()

class AboutDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        l = Label(self.top, text = "PyPaint v.5.0")
        l.pack()
