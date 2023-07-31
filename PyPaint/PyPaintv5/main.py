from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import numpy as np
from PIL import Image
from pixels import Pixel
from dialogs import SizeChooserDialog, AboutDialog
import math
import random

root = Tk()
root.title("PyPaint 5")

w, h = 10, 10
sw, sh = 60, 42
W, H = w * sw, h * sh
field = np.array([[None]*sh]*sw, Pixel)
color = (0, 0, 0)
size = 0
tool = 0 # 0-draw 1-delete 2-fill

def array_to_color(array):
    return '#%02X%02X%02X'%array

def colorPicker():
    global color
    fcolor = askcolor(title='Pick a color')[0]
    if fcolor == None:
        return
    color = (
        math.floor(fcolor[0]),
        math.floor(fcolor[1]),
        math.floor(fcolor[2])
    )
    currentcolor.configure(bg = array_to_color(color))
def aboutDialog():
    d = AboutDialog(root)
    root.wait_window(d.top)
def changecanvsize():
    d = SizeChooserDialog(root, getnewsize)
    root.wait_window(d.top)
def getnewsize(dialog):
    neww = int(dialog.ew.get())
    newh = int(dialog.eh.get())
    dialog.top.destroy()
    newfield = newcanvsize(neww, newh)
    redraw(newfield)
def newcanvsize(neww, newh):
    global sw, sh, W, H, canv, field
    sw, sh = neww, newh
    newfield = np.array([[None]*sh]*sw, Pixel)
    field = newfield
    canv.delete("all")
    W = w * sw
    H = h * sh
    canv.config(canv, width = W, height = H)
    canv.delete("all")
    return newfield
def redraw(newfield):
    global field
    shape = field.shape
    for i in range(sw):
        for j in range(sh):
            if i < shape[0] and j < shape[1]:
                if field[i][j] != None:
                    newfield[i][j] = field[i][j]
                    x = newfield[i][j].x
                    y = newfield[i][j].y
                    rect = canv.create_rectangle(x * w, y * h, (x + 1) * w, (y + 1) * h, fill = array_to_color(newfield[x][y].color), width = 0)
                    newfield[i][j].rect = rect
    field = newfield
def changetool(newtool):
    global tool
    tool = newtool
    currenttool.configure(image = toolsphotolist[tool])
def addsize(k):
    global size
    if size + k < 30 and size + k >= 0:
        size += k
        currentsize.configure(text = str(size+1))
def openfile():
    global field
    filename = filedialog.askopenfilename(initialdir = "/",title = "Open file")
    if filename == '':
        return
    image = Image.open(filename)
    if image.mode == 'RGB':
        pixels = image.load()
        shape = image.size
        newfield = newcanvsize(shape[0], shape[1])
        for i in range(shape[0]):
            for j in range(shape[1]):
                color = pixels[i, j]
                rect = canv.create_rectangle(i * w, j * h, (i + 1) * w, (j + 1) * h,
                                             fill=array_to_color(color), width=0)
                newfield[i][j] = Pixel(i, j, color, rect)
        field = newfield
    else:
        print("Unknown mode ", image.mode)
def savefile():
    filePath = filedialog.asksaveasfilename(initialdir = "/",title = "Save as")
    if filePath == '':
        return
    image = Image.new('RGB', (sw, sh))
    pixels = image.load()
    for i in range(sw):
        for j in range(sh):
            if field[i][j] != None:
                pixels[i, j] = field[i][j].color
            else:
                pixels[i, j] = (255, 255, 255)
    image.save(filePath)
menubar = Menu(root)

file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label ='Save as...', command = savefile)
file.add_command(label ='Open...', command = openfile)
file.add_command(label ='Exit', command = root.destroy)

edit = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Edit', menu = edit)
edit.add_command(label ='Change size...', command = changecanvsize)

help = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help)
help.add_command(label ='About', command = aboutDialog)

toolsframe = Frame(root)
canv = Canvas(root, width = W, height = H)
colorphoto = PhotoImage(file = r"Include/colorbutton.png")
pencilphoto = PhotoImage(file = r"Include/pencil.png")
eraserphoto = PhotoImage(file = r"Include/eraser.png")
sizeplusphoto = PhotoImage(file = r"Include/sizeplus.png")
sizeminusphoto = PhotoImage(file = r"Include/sizeminus.png")
toolsphotolist = (pencilphoto, eraserphoto)
colorbutton = Button(toolsframe, image = colorphoto, command = colorPicker)
currentcolor = Label(toolsframe, width = 5, height = 2, bg = array_to_color(color))
pencilbutton = Button(toolsframe, image = pencilphoto, command = lambda: changetool(0))
eraserbutton = Button(toolsframe, image = eraserphoto, command = lambda: changetool(1))
currenttool = Label(toolsframe, image = pencilphoto)
sizeplusbutton = Button(toolsframe, image = sizeplusphoto, command = lambda: addsize(1))
sizeminusbutton = Button(toolsframe, image = sizeminusphoto, command = lambda: addsize(-1))
currentsize = Label(toolsframe, width = 5, text = "1")

def draw(x, y):
    if tool == 0:
        if field[x][y] == None:
            pixelcolor = array_to_color(color)
            rect = canv.create_rectangle(x * w, y * h, (x + 1) * w, (y + 1) * h, fill = pixelcolor, width = 0)
            field[x][y] = Pixel(x, y, color, rect)
        else:
            field[x][y].color = color
            canv.itemconfig(field[x][y].rect, fill = array_to_color(field[x][y].color))
            canv.itemconfig(field[x][y].rect, outline = array_to_color(field[x][y].color))

    elif tool == 1:
        if(field[x][y] != None):
            canv.delete(field[x][y].rect)
            field[x][y] = None
def mouseEvent(e):
    global space
    x = math.floor(e.x / w)
    y = math.floor(e.y / h)
    if x < 0 or y < 0 or x >= sw or y >= sh:
        return
    for i in range(size + 1):
        for j in range(size + 1):
            dotx = x - i + math.floor(size/2)
            doty = y - j  + math.floor(size/2)
            if dotx >= 0 and doty >= 0 and dotx < sw and doty < sh:
                draw(dotx, doty)
def main():
    root.after(10, main)
main()
canv.bind("<Button-1>", mouseEvent)
canv.bind("<B1-Motion>", mouseEvent)
toolsframe.pack()
colorbutton.pack(side=LEFT)
currentcolor.pack(side=LEFT)
pencilbutton.pack(side=LEFT)
eraserbutton.pack(side=LEFT)
currenttool.pack(side=LEFT)
sizeplusbutton.pack(side=LEFT)
currentsize.pack(side=LEFT)
sizeminusbutton.pack(side=LEFT)
canv.pack()
root.config(menu = menubar)
root.mainloop()
