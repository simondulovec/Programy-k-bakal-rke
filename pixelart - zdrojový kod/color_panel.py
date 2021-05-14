from tkinter import *
from tkcolorpicker import askcolor
from config import *
from PIL import Image, ImageTk

class ColorPanel(Canvas):

    def __init__(self, master, messages):
        super().__init__(master, bg = "green", bd = 0)
        self.place(x = 1235, y = 5, width = 200, height = 200)
        self.create_widgets()
        self.messages = messages
        self.mouse_img = ImageTk.PhotoImage(Image.open("mouse.png"))
        self.create_image(0, 0, image = self.mouse_img, anchor = NW)


    def create_widgets(self):
        self.left_button = Button(self, text = "L", command = self.change_left_color, bd = 0, bg = "red")
        self.left_button.place(x = 60, y = 40, width = 30, height = 30)
        self.right_button = Button(self,text = "R", command = self.change_right_color, bd = 0, bg = "blue")
        self.right_button.place(x = 110, y = 40, width = 30, height = 30)

    def change_left_color(self):
        self.left_color = askcolor()
        #bug fixed, when cancel is pressed in tkcolorpicker None colors are selected, instead previous color is unchanged
        if self.left_color[HEXA] is not None:
            self.messages["colors"][LEFT_BUTTON] = self.left_color[RGB]
            self.messages["colors"][PREV_LEFT_BUTTON] = self.left_color[RGB]
            self.left_button.config(bg = self.left_color[HEXA])

    def change_right_color(self):
        self.right_color = askcolor()
        #bug fixed, when cancel is pressed in tkcolorpicker None colors are selected, instead previous color is unchanged
        if self.right_color[HEXA] is not None:
            self.messages["colors"][RIGHT_BUTTON] = self.right_color[RGB]
            self.right_button.config(bg = self.right_color[HEXA])
