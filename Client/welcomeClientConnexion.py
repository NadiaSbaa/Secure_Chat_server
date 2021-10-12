from PIL import Image, ImageTk
import tkinter as tk
import time

IMAGE_PATH = '../images/insat2.png'
WIDTH, HEIGTH = 1200, 700

screen = tk.Tk()
screen.geometry('{}x{}'.format(WIDTH, HEIGTH))

canvas = tk.Canvas(screen, width=WIDTH, height=HEIGTH)
canvas.pack()

img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize(
    (WIDTH, HEIGTH), Image.ANTIALIAS))
# Keep a reference in case this code is put in a function.
canvas.background = img
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)


screen.after(4500, screen.destroy)
screen.mainloop()
if True:
   import client_connection