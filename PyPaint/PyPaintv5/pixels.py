from tkinter import *
from tkinter.colorchooser import askcolor
import numpy as np
from PIL import Image
import math
import random

class Pixel():
    def __init__(self, x, y, color, rect):
        self.x = x
        self.y = y
        self.color = color
        self.rect = rect
