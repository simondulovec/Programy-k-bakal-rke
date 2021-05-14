from tkinter import *
from config import *
class Cell():

    def __init__(self,x=0,y=0,color="white",size = CELL_INIT_SIZE):
        self.x=x
        self.y=y
        self.color = TRANSPARENT_COLOR_HEXA
        self.size=size

    def set_location(self,x,y):
        self.x=x
        self.y=y

    def set_size(self, size):
        self.size = size

    def render(self,canvas):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=self.color)
