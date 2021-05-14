from tkinter import *
from config import *
import controller as cl
import app_menu as am

class App(Frame):

    def __init__(self,master = None, **kwargs):
        self.options = {"master":master, **kwargs}
        super().__init__(**self.options)

        self.xbar = Scrollbar(self, orient=HORIZONTAL)
        self.ybar = Scrollbar(self)
        self.item_canvas = Canvas(self, width = 1920, height = 1080,
                                     xscrollcommand=self.xbar.set,
                                     yscrollcommand=self.ybar.set)
        
        self.container = Frame(master = self.item_canvas, **kwargs)
        self.item_canvas.create_window(0,0, window = self.container, anchor = NW)

        self.xbar.configure(command=self.item_canvas.xview)
        self.ybar.configure(command=self.item_canvas.yview)

        self.item_canvas.configure(scrollregion=(0,0,1900,980))
        self.item_canvas.configure(background='black')
        

        self.xbar.pack(side = BOTTOM, fill = X)
        self.ybar.pack(side = RIGHT, fill = Y)
        self.item_canvas.pack(side = LEFT, expand = TRUE, fill = BOTH)
            
        self.controller = cl.Controller(master = self.container)
        self.pack()

    def get_controller(self):
        return self.controller

if __name__== "__main__":
    root = Tk()
    root.title("pixelart")
    app = App(master = root, **FRAME_INIT)
    root.config(menu = app.get_controller().get_view().get_menu_bar())
    app.mainloop()


