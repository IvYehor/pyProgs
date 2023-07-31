from tkinter import *

root = Tk()

canv = Canvas(root, width=500, height=250)
canv.pack()

radiovar = StringVar()
rb1=Radiobutton(root,text='red',variable=radiovar,value='red')
rb2=Radiobutton(root,text='green',variable=radiovar,value='green')
rb3=Radiobutton(root,text='blue',variable=radiovar,value='blue')
rb1.pack()
rb2.pack()
rb3.pack()

instrvar = StringVar()
brush=Radiobutton(root,text='Brush',variable=instrvar,value='brush')
fill=Radiobutton(root,text='Fill',variable=instrvar,value='fill')
earase=Radiobutton(root,text='Earase',variable=instrvar,value='earase')
brush.pack()
fill.pack()
earase.pack()

scale1 = Scale(root,orient=HORIZONTAL,length=300,from_=10,to=80,tickinterval=5,
 resolution=5)
scale1.pack()


canv.create_rectangle(0, 0, 500, 250, fill="white")



def draw(event):
 scl = scale1.get()
 rad = radiovar.get()
 instr = instrvar.get()
 x = event.x
 y = event.y
 if instr == 'brush':
  canv.create_rectangle(x - scl, y - scl, x + scl, y + scl, fill=rad, outline=rad)
 elif instr == 'fill':
  canv.create_rectangle(0, 0, 500, 250, fill=rad)
 elif instr == 'earase':
  canv.create_rectangle(x - scl, y - scl, x + scl, y + scl, fill="white", outline="white")

canv.bind('<B1-Motion>',draw)

root.mainloop()
