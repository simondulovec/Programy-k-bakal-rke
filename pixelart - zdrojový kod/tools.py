from tkinter import *
from config import *
from PIL import ImageTk

class Tools(LabelFrame):

    def __init__(self, master, messages):
        super().__init__(master, bg = "white", bd = 0)
        self.place(x = 1235, y = 210, width = 200, height = 100)
        self.create_widgets()
        self.messages = messages

    def create_widgets(self):
        self.pencil_img = ImageTk.PhotoImage(file ="pencil.png")
        self.pen = Button(self, bd = 0, bg = "#4d4d4d", command = self.set_pen, image = self.pencil_img)
        self.pen.place(x = 10, y = 10, width = 30, height = 30)
        self.eracer_img = ImageTk.PhotoImage(file ="eracer.png")
        self.eraser = Button(self, bd = 0, bg = "#4d4d4d", command = self.set_eraser, image = self.eracer_img)
        self.eraser.place(x = 42, y = 10, width = 30, height = 30)
        self.spray_img = ImageTk.PhotoImage(file ="spray.png")
        self.spray = Button(self, bd = 0, bg = "#4d4d4d", command = self.set_spray, image = self.spray_img)
        self.spray.place(x = 74, y = 10, width = 30, height = 30)
        #self.circle = Button(self, text = "C", bd = 0, bg = "#ff0000", command = self.set_circle)
        #self.circle.place(x = 10, y = 45, width = 30, height = 30)
        
    def set_eraser(self):
        self.messages["change_tool"] = True
        self.messages["tool"] = ERASER
        self.messages["tool_cursor"] = "X_cursor"
        self.messages["colors"][LEFT_BUTTON] = TRANSPARENT_COLOR_RGB

    def set_pen(self):
        self.messages["change_tool"] = True
        self.messages["tool"] = PEN
        self.messages["tool_cursor"] = "pencil"
        self.messages["colors"][LEFT_BUTTON] = self.messages["colors"][PREV_LEFT_BUTTON]

    def set_spray(self):
        self.messages["change_tool"] = True
        self.messages["tool"] = SPRAY
        self.messages["tool_cursor"] = "spraycan"
        self.messages["colors"][LEFT_BUTTON] = self.messages["colors"][PREV_LEFT_BUTTON]

    def set_circle(self):
        self.messages["change_tool"] = True
        self.messages["tool"] = CIRCLE
        self.messages["tool_cursor"] = "dot"
        self.messages["colors"][LEFT_BUTTON] = self.messages["colors"][PREV_LEFT_BUTTON]
