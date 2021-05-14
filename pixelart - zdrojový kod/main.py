from tkinter import *
from config import *
import part as pt
from PIL import Image,ImageTk

class Main(LabelFrame):

    def __init__(self,master=None,var=None,messages=None,**kwargs):
        self.options={"master":master,**kwargs}
        super().__init__(**self.options)
        self.messages=messages
        self.var=var
        self.part_var=StringVar(value="empty")
        self.anim_var=StringVar(value = str(id(self)))
        #image for recognizing main
        self.picture=Image.new("RGBA",(self.messages["cells_x"], self.messages["cells_y"]),(255,255,255,255))
        self.add_layer_img = ImageTk.PhotoImage(file="add_layer.png")
        self.add_layer_from_file_img = ImageTk.PhotoImage(file="load_from_file.png")
        self.delete_image_img = ImageTk.PhotoImage(file="delete_image.png")
        self.in_anim_img = ImageTk.PhotoImage(file="in_anim.png")
        self.not_in_anim_img = ImageTk.PhotoImage(file="not_in_anim.png")
        self.pixels=self.picture.load()
        #fill up pixels with color RGB(254,254,254)
        self.init_pixels()
        #resized image for main GUI Label frame
        self.create_picture()
        self.create_widgets()
        #self.bind_buttons()
        self.parts={}
        self.pack(side=LEFT)

    def create_widgets(self):
        #anim button
        self.anim_button = Checkbutton(master=self, selectcolor = "#0c398d" ,variable=self.anim_var, onvalue=str(id(self)),
                offvalue="None", indicatoron = False, command = self.update_anim_index, image = self.not_in_anim_img, 
                selectimage = self.in_anim_img, bd = 0, highlightthickness = 0, bg = "#e60000", activebackground = "#ff0000")
        self.anim_button.place(x = 7, y = 5, width = 94, height = 15)
        #canvas + scrollable frame
        self.canvas=Canvas(master=self,bg="#4d4d4d",bd=0, highlightthickness = 0)
        self.canvas.place(x=7,y=162,width=94,height=120)
        self.scrollable_frame=LabelFrame(master=self.canvas,bg="#4d4d4d", bd = 0, highlightthickness = 0)
        self.canvas.create_window((0, 0),window=self.scrollable_frame,anchor="nw")
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(ALL)))
        #scrollbar
        self.scrollbar_y=Scrollbar(master=self.canvas)
        self.scrollbar_y.config(command=self.canvas.yview)
        self.scrollbar_y.place(x = 82, y = -1, width = 12, height = 121)
        self.canvas.config(yscrollcommand=self.scrollbar_y.set)
        #select main
        self.select_button=Radiobutton(self,variable=self.var,value=str(id(self)),bd=0,highlightthickness=0,command=self.set_display_layers, indicatoron = False, 
                bg = "#4d4d4d", activebackground = "#8c8c8c", image = self.final_picture, selectcolor = "#ff0000")
        self.select_button.place(x = 7,y = 24, width=94, height=94)
        #add layer
        self.add_layer_button=Button(self,text="add layer",bd=0,command=self.set_add_part, image = self.add_layer_img, highlightthickness = 0, bg = "#00b300", activebackground = "#00cc00")
        self.add_layer_button.place(x=7,y=122,width=94,height = 15)
        #add layer from file
        self.add_layer_from_file_button=Button(self,bd=0,command=self.set_import_as_layer, image = self.add_layer_from_file_img, highlightthickness = 0, bg = "#145feb", activebackground = "#2c6fed")
        self.add_layer_from_file_button.place(x=7,y=142,width=94,height = 15)
        #delete main
        self.delete_button=Button(self,bd=0,text="delete",command=self.set_garbage, bg = "#e60000", highlightthickness = 0, image = self.delete_image_img, activebackground = "red")
        self.delete_button.place(x=7,y=286,width=94,height=15)

    def update_anim_index(self):
        self.messages["anim_index"] = 0

    def create_picture(self):
        self.resized_picture=self.picture.resize((90,90))
        self.final_picture=ImageTk.PhotoImage(self.resized_picture)

    def init_pixels(self):
        for i in range(self.messages["cells_y"]):
            for j in range(self.messages["cells_x"]):
                self.pixels[j,i]=(254,254,254)

    def update_pixel(self,x,y,color):
        self.pixels[x,y]=color

    def update_picture(self,x,y,color):
        self.pixels[x,y]=color
        self.create_picture() 
        self.set_picture()

    def set_picture(self):
        self.select_button.config(image=self.final_picture)

    def set_garbage(self):
        self.messages["remove_main"]=True
        self.messages["main_id"]=str(id(self))

    def set_add_part(self):
        self.messages["add_part"]=True
        self.messages["main_id"]=str(id(self))

    def set_display_layers(self):
        #checking for main/image with no layers
        if len(self.parts) > 0:
            self.messages["display_layers"]=True
            self.messages["drawing_enabled"]=True
            self.messages["main_id"]=str(id(self))
        else:
            self.messages["drawing_enabled"]=False
      
    def add_part(self):
        new_part=pt.Part(master=self.scrollable_frame,main_id=str(id(self)),var=self.part_var,messages=self.messages) 
        self.parts[str(id(new_part))]=new_part
        #setting part var so trimode is not enabled 
        self.part_var.set(str(id(new_part)))
        #this message is for data in model
        self.messages["part_id"]=str(id(new_part))
        self.drawing_enabled=True

    def reset_parts_value(self):
        self.part_val=0
        for i in self.parts:
            i.val=self.part_val
            i.part_name.config(onvalue=self.part_val)
            i.var.set(self.part_val)
            i.part_name.config(variable=i.var)
            self.part_val+=1

    def get_parts(self):
        return self.parts

    def get_part(self, part_id):
        return self.parts[part_id]

    def is_empty(self):
        if len(self.parts) == 0:
            return True
        else:
            return False

    def set_import_as_layer(self):
        self.messages["import_as_layer"] = True
