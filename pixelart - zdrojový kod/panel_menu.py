from tkinter import *
from PIL import ImageTk
class PanelMenu(LabelFrame):

    def __init__(self,master=None,messages=None):
        super().__init__(master=master,width=110,height=321,bg="#4d4d4d",bd=0,highlightthickness=1)
        self.messages=messages
        self.add_image_img = ImageTk.PhotoImage(file = "add_layer.png")
        self.load_from_file_img = ImageTk.PhotoImage(file = "load_from_file.png")
        self.create_widgets()
        self.bind_buttons()
        self.pack(side=LEFT)

    def create_widgets(self):
        self.add_main=Button(master=self,image=self.add_image_img,bd=0,highlightthickness=0, bg = "#00b300", activebackground = "#00cc00")
        self.add_main.place(x=7,y=5,width=94,height=15)

        self.add_main_from_file=Button(master=self,image=self.load_from_file_img,bd=0,highlightthickness=0, bg = "#145feb", activebackground = "#2c6fed")
        self.add_main_from_file.place(x=7,y=25,width=94,height=15)

        #commands
        self.add_main_from_file.configure(command = self.set_import_as_image)

    def bind_buttons(self):
        self.add_main.config(command=self.set_add_main)

    def set_add_main(self):
        self.messages["add_main"] = True

    def set_import_as_image(self):
        self.messages["import_as_image"] = True
