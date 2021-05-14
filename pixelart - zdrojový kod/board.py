from tkinter import *
import main as mn
from config import *

class Board(Canvas):

    def __init__(self, master = None, messages = None, **kwargs):
        self.options = {"master":master, **kwargs}
        super().__init__(**self.options)
        self.var = StringVar(value = "empty")
        self.messages = messages
        self.create_widgets()
        self.place(x = BOARD_INIT_PX, y = BOARD_INIT_PY, width = BOARD_INIT_WIDTH, height = BOARD_INIT_HEIGHT)
        self.mains = {}

    def create_widgets(self):
        #scrollable frame
        self.scrollable_frame = LabelFrame(master = self, bg = "#e6e6e6", bd = 0, highlightthickness = 0)           
        self.create_window((0,0),window=self.scrollable_frame,anchor="nw")
        #scrollbar
        self.scrollbar_x=Scrollbar(master=self,orient=HORIZONTAL)
        self.scrollbar_x.config(command=self.xview)
        self.scrollbar_x.pack(side=BOTTOM,fill=X)
        self.config(xscrollcommand=self.scrollbar_x.set)
        #binding trigger whenever scrollbar size changes (main is added or removed)
        self.scrollable_frame.bind("<Configure>",lambda e: self.configure(scrollregion=self.bbox(ALL)))

    def add_main(self):
        new_main=mn.Main(master=self.scrollable_frame,var=self.var,messages=self.messages,**MAIN_INIT)
        self.mains[str(id(new_main))]=new_main
        #this message is for data in model
        self.messages["main_id"]=str(id(new_main))
        self.messages["hover_id"]=str(id(new_main))
        self.var.set(str(id(new_main)))
        self.drawing_enabled=True

    def get_main(self,main_id):
        return self.mains[main_id]

    def get_current_main_id(self):
        return self.var.get()

    def get_current_part_id(self):
        #checking for empty project/grid or (no image/main created)
        if self.var.get() == "empty":
            return "empty"
        else:
            return self.mains[self.var.get()].part_var.get()

    def get_mains(self):
        return self.mains

    def clear(self):
        for key in self.mains:
            self.mains[key].destroy()
        self.mains.clear()

    def is_empty(self):
        if len(self.mains) == 0:
            return True
        else:
            return False
