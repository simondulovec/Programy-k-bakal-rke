import panel as pn
import grid as gd
import anim as an
import color_panel as cp
import tools as ts
import app_menu as am
from config import *
from tkinter import *

class View():
    def __init__(self,master):
        self.master=master
        self.messages={"add_main":False,"display_layers":False,"main_id":None,"add_part":False,"remove_main":False,
                "remove_part":False,"part_id":None,"draw_single":False,"draw_multiple":False,"spray":False,"which_button":0,"event":None,"draw_release":False,
                "play_anim":False,"stop_anim":False,"anim_playing":False,"drawing_enabled":True,"colors":[PEN_INIT_LEFT_COLOR, PEN_INIT_RIGHT_COLOR, PEN_INIT_LEFT_COLOR],"fps":FPS_INIT,
                "change_tool":False,"tool":PEN,"tool_cursor":"pencil","pen_hover":False,"circle_hover":False,"tool_hover_color":None,"hover_id":None, "tool_leave":False,
                "draw_circle":False, "cell_size":CELL_INIT_SIZE,"cells_x":CELLS_X_INIT, "cells_y":CELLS_Y_INIT, "grid_max_x":GRID_MAX, "grid_max_y":GRID_MAX, "cursor_x":0, 
                "cursor_y":0, "new_project":False, "create_new_project":False,"new_project_width":NEW_PROJECT_INIT_SIZE_X, "new_project_height":NEW_PROJECT_INIT_SIZE_Y, "anim_index":0,
                "export":False, "import_as_image":False, "import_as_layer":False, "save_project": False, "exit": False, "new_project_name": "New Project", "copy_from_image_id": None,
                "what_is_copied":None, "copy_from_part_id": None, "open_project": False, "show_help": False}
        self.menu_bar = am.AppMenu(master.master, self.messages)
        self.anim = an.Anim(master, self.messages, **ANIM_INIT)
        self.panel = pn.Panel(master, self.messages, **PANEL_INIT)
        self.grid = gd.Grid(master, self.panel, self.messages, **GRID_INIT)
        self.color_panel=cp.ColorPanel(master,self.messages)
        self.tools = ts.Tools(master, self.messages)
        self.width_var = StringVar(value = 32)
        self.height_var = StringVar(value = 30)
        self.name_var = StringVar(value = "New Project")

#=============================MESSAGES===========================
#"hover_id" = id for playing animation
#"what_is_copied" = depends on data which are being copied (image/layer)
        
#=============================COMPONENTS==========================
    def get_menu_bar(self):
        return self.menu_bar

    def get_main_id(self):
        return self.messages["main_id"]

    def get_part_id(self):
        return self.messages["part_id"]

    def unset_main_part_id(self):
        self.messages["main_id"]=None
        self.messages["part_id"]=None

    def unset_add_main(self):
        self.messages["add_main"]=False

    def unset_display_layers(self):
        self.messages["display_layers"]=False
        self.unset_main_id()

    def unset_add_part(self):
        self.messages["add_part"]=False
        self.unset_main_id()

    def unset_main_id(self):
        self.messages["main_id"]=None

    def unset_remove_main(self):
        self.messages["remove_main"]=False
        self.unset_main_id()

    def unset_remove_part(self):
        self.messages["remove_part"]=False
        self.unset_main_part_id()

#==========================DRAWING================================

    def set_drawing_enabled(self):
        self.messages["drawing_enabled"] = True

    def unset_drawing_enabled(self):
        self.messages["drawing_enabled"]=False 

    def unset_draw_single(self):
        self.messages["draw_single"]=False

    def unset_draw_multiple(self):
        self.messages["draw_multiple"]=False

    def unset_draw_release(self):
        self.messages["draw_release"]=False

    def unset_play_anim(self):
        self.messages["play_anim"] = False
    
    def unset_stop_anim(self):
        self.messages["stop_anim"] = False

    def unset_change_tool(self):
        self.messages["change_tool"] = False

    def unset_spray(self):
        self.messages["spray"] = False

    def unset_draw_circle(self):
        self.messages["draw_circle"] = False

    def unset_pen_hover(self):
        self.messages["pen_hover"] = False

    def unset_tool_leave(self):
        self.messages["tool_leave"] = False

    def unset_circle_hover(self):
        self.messages["circle_hover"] = False

#========MENU_BAR=============================================
    def unset_new_project(self):
        self.messages["new_project"] = False

    def unset_create_new_project(self):
        self.messages["create_new_project"] = False

    def unset_import_as_image(self):
        self.messages["import_as_image"] = False

    def unset_import_as_layer(self):
        self.messages["import_as_layer"] = False

    def unset_save_project(self):
        self.messages["save_project"] = False

    def unset_open_project(self):
        self.messages["open_project"] = False

    def unset_exit(self):
        self.messages["exit"] = False

    def unset_show_help(self):
        self.messages["show_help"] = False

#=============================================================

    def unset_export(self):
        self.messages["export"] = False

    def add_main(self):
        self.panel.board.add_main()

    def get_main(self,main_id):
        return self.panel.board.mains[main_id]

    def get_part(self,main_id,part_id):
        return self.panel.board.mains[main_id].parts[part_id]

    def new_project(self):
        self.new_project_window = Toplevel(self.master.master)
        self.new_project_window.title("New Project")
        #project name
        self.project_name = Label(master = self.new_project_window, text = "Project name:")
        self.project_name.place(x = 15, y = 50, width = 100, height = 30)
        self.name_entry = Entry(master = self.new_project_window, bd = 0, highlightthickness = 0, textvariable = self.name_var)
        self.name_entry.place(x = 125, y = 50, width = 150, height = 30)
        #image width
        self.image_width = Label(master = self.new_project_window, text = "Image size:")
        self.image_width.place(x = 25, y = 100, width = 100, height = 30)
        self.width_entry = Entry(master = self.new_project_window, bd = 0, highlightthickness = 0, textvariable = self.width_var)
        self.width_entry.place(x = 125, y = 100, width = 50, height = 30)
        self.width_px = Label(master = self.new_project_window, text = "px")
        self.width_px.place(x = 175, y = 100, width = 30, height = 30)
        #buttons
        self.create = Button(master = self.new_project_window, text = "Create", command = self.set_create_new_project)
        self.create.place(x = 175, y = 325, width = 80, height = 40)
        self.cancel = Button(master = self.new_project_window, text = "Cancel", command = self.new_project_window.destroy)
        self.cancel.place(x = 45, y = 325, width = 80, height = 40)

        #first two numbers are size, second two numbers are position
        self.new_project_window.geometry("%dx%d%+d%+d" % (NEW_PROJECT_INIT_WIDTH, NEW_PROJECT_INIT_HEIGHT, NEW_PROJECT_PX, NEW_PROJECT_PY))
        #this will asure that window stay on top
        self.new_project_window.attributes('-topmost', 'true')

    def set_create_new_project(self):
        self.new_project_window.destroy()
        self.messages["new_project_width"] = self.width_var.get()
        self.messages["new_project_height"] = self.width_var.get()
        self.messages["new_project_name"] = self.name_var.get()
        self.messages["create_new_project"] = True
