from tkinter import *

class AppMenu(Menu):

    def __init__(self,master = None, messages = None):
        super().__init__(master = master, bd = 0)
        self.filemenu = Menu(self, tearoff = 0, bd = 0)
        self.helpmenu = Menu(self, tearoff = 0, bd = 0)
        self.add_cascade(label  = "File", menu = self.filemenu)
        self.add_cascade(label  = "Help", menu = self.helpmenu)
        self.messages = messages
    
    #file
        self.filemenu.add_command(label="New project    Ctrl+N", command = self.set_new_project)
        #self.filemenu.add_command(label="Save")
        self.filemenu.add_command(label="Open project   Ctrl+O", command = self.set_open_project)
        self.filemenu.add_command(label="Save project as           Ctrl+S", command = self.set_save_project)
        
        self.filemenu.add_separator()

        self.filemenu.add_command(label="Import as image", command = self.set_import_as_image)
        self.filemenu.add_command(label="Import as layer", command = self.set_import_as_layer)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Export images", command = self.set_export)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command = self.set_exit)

    #help
        self.helpmenu.add_command(label="Shortcuts and Info", command = self.set_show_help)

    def set_new_project(self):
        self.messages["new_project"] = True

    def set_export(self):
        self.messages["export"] = True

    def set_import_as_image(self):
        self.messages["import_as_image"] = True

    def set_import_as_layer(self):
        self.messages["import_as_layer"] = True

    def set_save_project(self):
        self.messages["save_project"] = True

    def set_open_project(self):
        self.messages["open_project"] = True
    
    def set_show_help(self):
        self.messages["show_help"] = True

    def set_exit(self):
        self.messages["exit"] = True
