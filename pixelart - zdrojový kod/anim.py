from tkinter import *
from PIL import Image,ImageTk
from config import *

class Anim(LabelFrame):

    def __init__(self, master, messages = None, **kwargs):
        self.options = {"master": master, **kwargs}
        super().__init__(**self.options)
        self.place(x = ANIM_INIT_PX, y = ANIM_INIT_PY, width = ANIM_INIT_WIDTH, height = ANIM_INIT_HEIGHT)
        self.var = IntVar(value = 5)
        self.label_var = StringVar(value = "FPS")
        self.messages = messages
        self.play_img = ImageTk.PhotoImage(file = "play.png")
        self.stop_img = ImageTk.PhotoImage(file = "stop.png")
        self.create_widgets()
       
    def create_widgets(self):
        #creating canvas and image
        self.canvas = Canvas(master = self, **ANIM_CANVAS_INIT)
        self.canvas.place(x = ANIM_CANVAS_INIT_PX, y = ANIM_CANVAS_INIT_PY, width = ANIM_CANVAS_INIT_WIDTH, height = ANIM_CANVAS_INIT_HEIGHT)
        self.image = Image.new("RGBA", (self.messages["cells_x"], self.messages["cells_y"]), (255,255,255,255))
        self.pixels = self.image.load()
        self.create_image()
        #buttons
        self.play_button = Button(master = self, command = self.play_anim, bd = 0, image = self.play_img, bg = "#00b300", activebackground = "#00cc00", highlightthickness = 0)
        self.play_button.place(x = 209, y = 602, width = 45, height = 45)
        self.stop_button = Button(master = self, command = self.stop_anim, bd = 0, image = self.stop_img, bg = "#e60000", activebackground = "#ff0000", highlightthickness = 0)
        self.stop_button.place(x = 258,y = 602, width = 45,height = 45)
        #scale
        self.fps = Scale(master = self, variable = self.var, orient = HORIZONTAL, from_ = 1, to = 60, command = self.set_fps, bg = "#4d4d4d", highlightthickness = 0, fg = "white")
        self.fps.place(x = 48,y = 602, width = 150, height = 45)
        #label
        self.label = Label(master = self, textvariable = self.label_var, bg = "#4d4d4d", highlightthickness = 0, fg = "white")
        self.label.place(x = 3, y = 602, width = 45, height = 45)
        #pading
        self.pad = Label(master = self, bg = "#4d4d4d", bd = 0, highlightthickness = 0)
        self.pad.place(x = 198, y = 602, width = 8, height = 45)

    def play_anim(self):
        self.messages["fps"] = self.var.get()
        self.messages["play_anim"] = True

    def stop_anim(self):
        self.messages["stop_anim"] = True

    def set_fps(self,val):
        self.messages["fps"] = self.var.get()

    def create_image(self):
        self.resized_picture = self.image.resize((ANIM_CANVAS_INIT_WIDTH, ANIM_CANVAS_INIT_HEIGHT), Image.NEAREST)
        self.final_image = ImageTk.PhotoImage(self.resized_picture)
        self.canvas.create_image((0,0), image = self.final_image, anchor = NW)

    def clear_image(self):
        for y in range(self.messages["cells_y"]):
            for x in range(self.messages["cells_x"]):
                self.pixels[x,y] = (255,255,255,255)

    def update_from_data(self, pixels):
        for y in range(self.messages["cells_y"]):
            for x in range(self.messages["cells_x"]):
                self.pixels[x,y] = pixels[x,y]
        self.create_image()

    def reset_anim(self):
        self.image = Image.new("RGBA", (self.messages["cells_x"], self.messages["cells_y"]), (255,255,255,255))
        self.pixels = self.image.load()
        self.canvas.delete("all")
        #self.clear_image()
        self.create_image()

