import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


f = open("demofile0.txt","r")
array = [f.readline().split()]
arrayf = []
for i in array[0]:
    print(i)
    arrayf.append(int(i))
npa = np.array(arrayf[0])
print(npa)

master = Tk()

canvas_width = 280
canvas_height = 280
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()
x1, y1, x2, y2 = 0, 0, 10, 10

count=0
for k in range(0, 28):
    for j in range(0, 28):
        number = arrayf[count]
        count +=1 
        color = "#" + str(hex(number)[2:5]) + \
            str(hex(number)[2:5]) + str(hex(number)[2:5])
        w.create_rectangle(x1, y1, x2, y2, fill=color)
        x1, x2 = x1 + 10, x2 + 10
    x1, y1, x2, y2 = 0, y1 + 10, 10, y2 + 10

mainloop()