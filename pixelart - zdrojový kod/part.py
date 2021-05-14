from tkinter import *
from PIL import Image,ImageTk

class Part(LabelFrame):

    def __init__(self,master=None,main_id=None,var=None,messages=None):
        super().__init__(master=master,bg="#808080", bd=0, highlightthickness=1,width=82,height=30, relief = "flat")
        self.image=PhotoImage()
        self.messages=messages
        self.main_id=main_id
        self.visibility_var=StringVar(value=str(id(self)))
        self.draw_var=var
        self.picture=Image.new("RGBA",(self.messages["cells_x"], self.messages["cells_y"]),(255,255,255,255))
        self.pixels=self.picture.load()
        self.create_picture()
        self.visible_img = ImageTk.PhotoImage(file="visible.png")
        self.not_visible_img = ImageTk.PhotoImage(file="not_visible.png")
        self.delete_layer_img = ImageTk.PhotoImage(file="delete_layer.png")
        self.create_widgets()
        self.pack(side=TOP)
         
    def create_widgets(self):
        self.draw_button=Radiobutton(master=self, variable=self.draw_var,value=str(id(self)),indicatoron=False,bd=0,highlightthickness=0, 
                bg = "#4d4d4d", selectcolor="#ff0000", image = self.final_picture, activebackground = "#8c8c8c")
        self.draw_button.place(x=2,y=2,width=24,height=24)

        self.visibility_button=Checkbutton(master=self,image=self.not_visible_img,bg = "#e60000",compound="bottom",variable=self.visibility_var,onvalue=str(id(self)),
                offvalue="None",command=self.set_display_layers, indicatoron = False, selectimage = self.visible_img, selectcolor = "#00b300", highlightthickness = 0, 
                activebackground = "#ff0000", bd = 0)
        self.visibility_button.place(x=28,y=2,width=24,height=24)

        self.remove_button=Button(master=self,image=self.delete_layer_img,command=self.set_remove_part, bd = 0, highlightthickness = 0, bg = "#e60000", activebackground = "#ff0000")
        self.remove_button.place(x=54,y=2,width=24,height=24)

    def create_picture(self):
        self.resized_picture=self.picture.resize((20,20))
        self.final_picture=ImageTk.PhotoImage(self.resized_picture)

    def update_picture(self,x,y,color):
        self.pixels[x,y]=color
        self.create_picture()
        self.set_picture()

    def update_pixel(self, x, y, color):
        self.pixels[x, y] = color

    def set_picture(self):
        self.draw_button.config(image=self.final_picture)

    def set_remove_part(self):
        self.messages["remove_part"]=True
        self.messages["main_id"]=self.main_id
        self.messages["part_id"]=str(id(self))

    def set_display_layers(self):
        self.messages["display_layers"]=True
        self.messages["main_id"]=self.main_id
