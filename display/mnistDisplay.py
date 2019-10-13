import mnistReader as r
from tkinter import *


master = Tk()

canvas_width = 280
canvas_height = 280
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()


x1, y1, x2, y2 = 0, 0, 10, 10
#x2, y2 = 10, 10

reader = r.Reader('../mnist/train-labels-idx1-ubyte.gz',
                  '../mnist/train-images-idx3-ubyte.gz')


image = [[0 for x in range(28)]
         for y in range(28)]
reader.getImageArray2D1(5678, image)

# print(image)

# image = reader.getArray()

for k in range(0, 28):
    for j in range(0, 28):
        number = image[k][j]
        color = "#" + str(hex(number)[2:5]) + \
            str(hex(number)[2:5]) + str(hex(number)[2:5])

        w.create_rectangle(x1, y1, x2, y2, fill=color)
        x1, x2 = x1 + 10, x2 + 10
    x1, y1, x2, y2 = 0, y1 + 10, 10, y2 + 10


mainloop()
