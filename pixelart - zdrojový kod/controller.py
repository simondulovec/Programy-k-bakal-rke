import view as vw
import model as md
from tkinter import *
from config import *
from tkinter import filedialog
from PIL import Image
import tkinter.messagebox as mb

class Controller():
    
    def __init__(self,master=None):
        self.master=master
        self.old_x=False
        self.old_y=False
        self.view=vw.View(master)
        self.model=md.Model(self.view.messages)
        self.controller_loop()
        self.prev_main = None
        #creating image after app start
        self.add_main()
        self.anim_id = None
        self.px = PX_INIT
        self.py = PY_INIT
        self.anim_list = []
        #shortcuts
        self.view.panel.bind("<Control-Key-i>", self.copy_image)
        self.view.panel.bind("<Control-Key-l>", self.copy_layer)
        self.view.panel.bind("<Control-Key-v>", self.paste_image_layer)
        self.view.panel.bind("<Control-Key-o>", self.open_project)
        self.view.panel.bind("<Control-Key-n>", self.init_new_project)
        self.view.panel.bind("<Control-Key-s>", self.init_save_project)
        #self.view.panel.bind("<Control-Shift-Key-i>", self.import_as_image)

#======================COPYING_IAMGES_AND_LAYERS========================================================
    def copy_image(self, event):
        self.view.messages["what_is_copied"]="nothing"
        if self.view.panel.board.is_empty():
            mb.showinfo("Pixelart", "Nothing to copy!")
        else:
            #save main id
            self.view.messages["copy_from_image_id"] = self.view.panel.board.get_current_main_id()
            if self.view.panel.board.get_main(self.view.messages["copy_from_image_id"]).is_empty():
                mb.showinfo("Pixelart", "Nothing to copy!")
            else:
                self.view.messages["what_is_copied"]="image"
                #print(self.view.messages["copy_from_image_id"])

    def copy_layer(self, event):
        self.view.messages["what_is_copied"]="nothing"
        if self.view.panel.board.is_empty():
            mb.showinfo("Pixelart", "Nothing to copy!")
        elif self.view.panel.board.get_main(self.view.panel.board.get_current_main_id()).is_empty():
            mb.showinfo("Pixelart", "Nothing to copy!")
        else:
            self.view.messages["copy_from_image_id"] = self.view.panel.board.get_current_main_id()
            self.view.messages["copy_from_part_id"] = self.view.panel.board.get_current_part_id()
            self.view.messages["what_is_copied"]="layer"

    def paste_image_layer(self, event):
#=======================================================PASTE_IMAGE===========================================
        if self.view.messages["what_is_copied"] == "image":
                self.generate_image()
#=======================================================PASTE_LAYER===========================================
        elif self.view.messages["what_is_copied"] == "layer":
            copy_from_image_id = self.view.messages["copy_from_image_id"]
            copy_from_part_id = self.view.messages["copy_from_part_id"]
            self.generate_layer()    
        else:
            mb.showinfo("Pixelart","Nothing to paste!")

    def generate_layer(self):
        self.view.messages["main_id"] = self.view.panel.board.get_current_main_id()
        self.add_part()
        copy_from_image_id = self.view.messages["copy_from_image_id"]
        copy_from_part_id = self.view.messages["copy_from_part_id"]
        value_from = self.model.data.data[copy_from_image_id][copy_from_part_id]
        self.view.messages["main_id"] = self.view.panel.board.get_current_main_id()
        self.view.messages["part_id"] = self.view.panel.board.get_current_part_id()
        for y in range(self.view.messages["cells_y"]):
            for x in range(self.view.messages["cells_x"]):
                self.update_view_model(x,y,value_from[x][y])
                 
    def generate_image(self):
        self.add_main()
        copy_from_image_id = self.view.messages["copy_from_image_id"]
        copy_to_image_id = self.view.panel.board.get_current_main_id()
        index = 0
        for key in self.model.data.data[copy_from_image_id].keys():
            index+=1
        for i in range(index - 1):
            #add_part() method reset "main_id", so i have to set it in every cycle iterration
            self.view.messages["main_id"] = self.view.panel.board.get_current_main_id()
            self.add_part()
        self.view.messages["main_id"] = self.view.panel.board.get_current_main_id() 
        for y in range(self.view.messages["cells_y"]):
            for x in range(self.view.messages["cells_x"]):
                for (key_from, value_from), (key_to, value_to) in zip(self.model.data.data[copy_from_image_id].items(), self.model.data.data[copy_to_image_id].items()):
                    self.view.messages["part_id"] = key_to
                    self.update_view_model(x,y, value_from[x][y])

#===============================SAVING_PROJECT==========================
    def save_project(self, path):
        project_file = self.create_project_file()
        try:
            with open(path + ".txt", "w") as txtf:
                txtf.write(project_file)
                mb.showinfo("Pixelart", "Project saved!")
        except:
            mb.showerror("Pixelart", "Saving project failed!")

    def create_project_file(self):
        project_file = ""
        project_file += (self.view.messages["new_project_name"] + "\n")
        project_file += "/\n"
        project_file += (str(self.view.messages["cells_x"]) + "x" + str(self.view.messages["cells_y"]) + "\n")
        for image, data in self.model.data.data.items():
            project_file += "/\n"
            for layer, layer_data in data.items():
                project_file +="*\n"
                for y in range(self.view.messages["cells_y"]):
                    for x in range(self.view.messages["cells_x"]):
                        project_file += (str(layer_data[y][x]) + "|")
                    project_file += "\n"
        return project_file

#==============================OPENING_PROJECT====================================    
    def open_project(self, event = None):
        path = filedialog.askopenfilename(title = "Open project", filetypes = [("txt file",".txt")])
        if path is not None and len(path) != 0:
            try:
                with open(path, "r") as txtf:
                    project_file = txtf.read()
            except:
                mb.showinfo("Pixelart", "Opening project failed!")
                return
            project_data = project_file.split("/")
        
            PROJECT_NAME = 0
            PROJECT_IMG_SIZE = 1

            #creating new project
            width = int(project_data[PROJECT_IMG_SIZE].split("x")[0])
            height = int(project_data[PROJECT_IMG_SIZE].split("x")[1])
            self.view.messages["cells_x"] = width
            self.view.messages["cells_y"] = height
            #image size description under grid
            self.view.grid.update_image_size()
            #setting new project name
            self.master.master.title(project_data[PROJECT_NAME])
            self.view.messages["grid_max_x"] = width - 1
            self.view.messages["grid_max_y"] = height - 1
            self.clear_old_project()

            for i in range(2, len(project_data)):
                self.add_main()
                layer_data = project_data[i].split("*")
                layer_data.pop(0)   #removing 0 element because its white symbol
                for j in range(len(layer_data) - 1):    # -1 because there is already part created in every new main
                    #setting main_id, because after add_part is called main_id is null
                    self.view.messages["main_id"] = self.view.panel.board.get_current_main_id()
                    self.add_part()

            mains = self.view.panel.board.get_mains()

            m_index = 2
            p_index = 0
            i = 0
            for y in range(height):
                for x in range(width):
                    m_index = 2
                    for main_key, main_value in mains.items():
                        p_index = 0
                        layer_data = project_data[m_index].split("*")
                        layer_data.pop(0)
                        m_index += 1
                        for part_key, part_value in main_value.get_parts().items():
                            data = layer_data[p_index].replace("\n","").split("|")
                            data.pop()  #last item is white space , so it have to be removed
                            self.view.messages["main_id"] = main_key
                            self.view.messages["part_id"] = part_key
                            color = tuple(map(int, data[i][1:-1].split(",")))
                            self.update_view_model(y,x, color)
                            p_index += 1
                    i += 1
                       
    def get_view(self):
        return self.view

    def clear_old_project(self):
        self.view.messages["drawing_enabled"] = False
        #if animation was runing, then is stopped and cleared
        if self.anim_id is not None:
            self.view.anim.after_cancel(self.anim_id)
            self.view.messages["anim_playing"] = False
            self.view.messages["anim_index"] = INDEX_INIT
            self.prev_main = None
        self.view.anim.reset_anim()
        #clearing GUI
        self.view.panel.board.clear()
        #clearing DATA
        self.model.data.clear()
        #clearing_grid
        self.view.grid.clear_cells()
        self.view.grid.create_cells()
        self.view.grid.reset_cell_size()
        self.view.grid.update_canvas_size()
        #reseting_cursor_position
        self.view.messages["pen_hover"] = False
        self.view.messages["cursor_x"] = 0
        self.view.messages["cursor_y"] = 0
        self.px = PX_INIT
        self.py = PY_INIT
        self.update_cursor_position()
        self.view.grid.update_image_size()

    def create_new_project(self):
        self.add_main()
    
    def add_main(self):
        #adding gui component
        self.view.panel.board.add_main()
        #adding data
        self.model.data.add_image(self.view.messages["main_id"])
        self.add_part()
        self.view.grid.clear_grid()
        self.view.unset_main_id()

    def add_part(self):
        #adding gui component
        self.view.panel.board.mains[self.view.messages["main_id"]].add_part()
        #adding data
        self.model.data.add_layer(self.view.messages["main_id"],self.view.messages["part_id"])
        if self.view.messages["main_id"] == self.view.panel.board.get_current_main_id():
            self.view.messages["drawing_enabled"]=True
        else:
            self.view.messages["drawing_enabled"]=False
        self.view.unset_add_part()
 
    def display_layers(self,main_id):
        self.view.grid.canvas.delete(ALL)
        for i in range(self.view.messages["cells_y"]):
            for j in range(self.view.messages["cells_x"]):
                #clearing grid and main image
                self.view.grid.reset_cell(j,i)
                self.view.get_main(main_id).update_pixel(j,i,TRANSPARENT_COLOR_RGB)
                for part_id,part in self.view.get_main(main_id).parts.items():
                    if part.visibility_var.get()!="None":
                        if self.model.data.get_color(main_id,part_id,j,i)!=TRANSPARENT_COLOR_RGB:
                            self.view.grid.set_color(j,i,self.from_rgb(self.model.data.get_color(main_id,part_id,j,i)))
                            self.view.get_main(main_id).update_pixel(j,i,self.model.data.data[main_id][part_id][j][i])
                self.view.grid.render_cell(j,i)
        self.view.get_main(main_id).create_picture()
        self.view.get_main(main_id).set_picture()

    def display_layer_pixel(self, main_id, x, y):
        self.view.grid.delete_cell(x, y)
        #clearing grid and main image
        self.view.grid.reset_cell(x,y)
        self.view.get_main(main_id).update_pixel(x,y,TRANSPARENT_COLOR_RGB)
        for part_id,part in self.view.get_main(main_id).parts.items():
            if part.visibility_var.get()!="None":
                if self.model.data.get_color(main_id,part_id,x,y)!=TRANSPARENT_COLOR_RGB:
                    self.view.grid.set_color(x,y,self.from_rgb(self.model.data.get_color(main_id,part_id,x,y)))
                    self.view.get_main(main_id).update_pixel(x,y,self.model.data.data[main_id][part_id][x][y])
        self.view.grid.render_cell(x,y)
        self.view.get_main(main_id).create_picture()
        self.view.get_main(main_id).set_picture()

    def update_anim_list(self):
        change = False
        self.anim_list.clear()
        for i in self.model.data.keys:
            main = self.view.panel.board.mains[i]
            if main.anim_var.get() != "None":
                self.anim_list.append(main)

    def anim_loop(self):
        self.update_anim_list()
        #changing button color when is currently displayed in animation
        if self.prev_main is not None:
            self.prev_main.anim_button.config(selectcolor = "#0c398d")
        #animation running only if at leat 1 iamge is checked
        if len(self.anim_list) > 0:
            self.view.anim.update_from_data(self.anim_list[self.view.messages["anim_index"]].pixels)
            self.prev_main = self.anim_list[self.view.messages["anim_index"]]
            self.anim_list[self.view.messages["anim_index"]].anim_button.config(selectcolor = "#2068ec")
            self.view.messages["anim_index"] += 1
            if self.view.messages["anim_index"] == len(self.anim_list):
                self.view.messages["anim_index"] = 0
        time = MS_IN_S // self.view.messages["fps"]
        self.anim_id = self.view.anim.after(time, self.anim_loop)

#CONTROLLER_LOOP#########################################################################################    
    def controller_loop(self):
        #starting animation
        if self.view.messages["play_anim"]:
            if self.view.messages["anim_playing"] == False:
                self.view.messages["anim_playing"] = True
                self.anim_loop()
            self.view.unset_play_anim()

        #stoping animation
        if self.view.messages["stop_anim"]:
            if self.view.messages["anim_playing"]:
                self.view.messages["anim_playing"] = False
                self.view.messages["anim_index"] = 0
                self.view.anim.after_cancel(self.anim_id)
            self.view.unset_stop_anim()
 
        #creating new main
        if self.view.messages["add_main"]:
            self.add_main()
            self.view.messages["drawing_enabled"]=True  
            self.view.unset_add_main()    
        
        #displaing layers
        if self.view.messages["display_layers"]:
            self.display_layers(self.view.messages["main_id"])
            self.view.unset_display_layers()
  
        #creating new parts
        if self.view.messages["add_part"]:
            self.add_part()
            
        #removing mains/images
        if self.view.messages["remove_main"]:
            if self.view.messages["anim_playing"]:
                mb.showinfo("Pixelart", "Stop animation fisrt!")
                self.view.unset_remove_main()
            elif mb.askyesno("","Are you sure you want to delete image?"):
                #hiding gui
                self.view.panel.board.mains[self.view.messages["main_id"]].pack_forget()
                #removing gui
                self.view.panel.board.mains.pop(self.view.messages["main_id"])
                #removing data
                self.model.data.data.pop(self.view.messages["main_id"])
                self.model.data.keys.remove(self.view.messages["main_id"])
                #removing main which is selected
                if self.view.messages["main_id"] == self.view.messages["copy_from_image_id"]:
                    #when source main is deleted, all data are lost, so copy, paste operations are disabled
                    self.view.messages["what_is_copied"] = "Source image was removed!"
                if self.view.messages["main_id"]==self.view.panel.board.get_current_main_id():
                    if len(self.view.panel.board.get_mains()) > 0:
                        #setting var to another main/image in dictionary
                        new_main_id = str(next(iter(self.view.panel.board.get_mains())))
                        self.view.panel.board.var.set(new_main_id)
                        #setting new hover_id
                        self.view.messages["hover_id"] = new_main_id
                        self.display_layers(new_main_id)
                        #checking for new selected main/image has no layers
                        if len(self.view.panel.board.get_main(new_main_id).get_parts()) == 0:
                            self.view.messages["drawing_enabled"]=False
                        else:
                            self.view.messages["drawing_enabled"]=True
                    else:
                        self.view.messages["what_is_copied"] = "Nothing to copy!"
                        self.view.grid.clear_grid()
                        self.view.unset_drawing_enabled()
                        self.view.messages["hover_id"] = None
                self.view.unset_remove_main()
            else:
                self.view.unset_remove_main()

        #removing parts/layers
        if self.view.messages["remove_part"]:
            if mb.askyesno("","Are you sure you want to delete layer?"):
                #hiding gui
                self.view.panel.board.mains[self.view.messages["main_id"]].parts[self.view.messages["part_id"]].pack_forget()
                #removing gui
                self.view.panel.board.mains[self.view.messages["main_id"]].parts.pop(self.view.messages["part_id"])
                #removing data
                self.model.data.data[self.view.messages["main_id"]].pop(self.view.messages["part_id"], None)
                #redrawing layers
                self.display_layers(self.view.messages["main_id"])
                if self.view.messages["part_id"] == self.view.messages["copy_from_part_id"]:
                    #when source main is deleted, all data are lost, so copy, paste operations are disabled
                    self.view.messages["what_is_copied"] = "Source was removed!"
                if self.view.messages["part_id"]==self.view.panel.board.get_current_part_id():
                    current_main = self.view.panel.board.get_main(self.view.messages["main_id"])
                    if len(current_main.get_parts()) > 0:
                        new_part_id = str(next(iter(current_main.get_parts())))
                        current_main.part_var.set(new_part_id)
                    else:
                        self.view.messages["what_is_copied"] = "Nothing to copy!"
                        self.view.grid.clear_grid()
                        self.view.unset_drawing_enabled()
                self.view.unset_remove_part()
            else:
                self.view.unset_remove_part()

#====================DRAWING============================================
        if self.view.messages["draw_single"]:
            x=self.view.messages["event"].x//self.view.messages["cell_size"]
            y=self.view.messages["event"].y//self.view.messages["cell_size"]
            #correcting out of bounds drawing
            if x >= self.view.messages["grid_max_x"]:
                x = self.view.messages["grid_max_x"]
            if x <= GRID_MIN:
                x = GRID_MIN
            if y >= self.view.messages["grid_max_y"]:
                y = self.view.messages["grid_max_y"]
            if y <= GRID_MIN:
                y = GRID_MIN
            button = self.view.messages["which_button"]
            color = self.view.messages["colors"][button]
            self.update_view_model(x, y, color)
            #if pixel from top layer is removed, coresponding pixel is redrawn, so bttoom layers are visible
            self.erasing(self.view.messages["main_id"], x, y)
            self.view.unset_draw_single()

        if self.view.messages["draw_multiple"]:
            #setting correct color depending on which mouse button was pressed
            button = self.view.messages["which_button"]
            color = self.view.messages["colors"][button]
            self.on_motion(self.view.messages["event"], color)
            self.view.unset_draw_multiple()

        if self.view.messages["draw_release"]:
            self.on_release()
            self.view.unset_draw_release()

        if self.view.messages["spray"]:
            #setting correct color depending on which mouse button was pressed
            button = self.view.messages["which_button"]
            color = self.view.messages["colors"][button]
            for y in range(self.view.messages["cells_y"]):
                for x in range(self.view.messages["cells_x"]):
                     self.update_cell(x, y, color)
                     self.update_main_pixel(self.view.messages["main_id"],x,y,color)
                     self.update_part_pixel(self.view.messages["main_id"],self.view.messages["part_id"],x,y,color)
                     self.update_data(self.view.messages["main_id"],self.view.messages["part_id"],x,y,color)

            self.view.panel.board.get_main(self.view.messages["main_id"]).create_picture()
            self.view.panel.board.get_main(self.view.messages["main_id"]).set_picture()

            self.view.panel.board.get_main(self.view.messages["main_id"]).get_part(self.view.messages["part_id"]).create_picture()
            self.view.panel.board.get_main(self.view.messages["main_id"]).get_part(self.view.messages["part_id"]).set_picture()

            self.display_layers(self.view.messages["main_id"])
            self.view.unset_spray()

#=======hovering===========================================
        if self.view.messages["pen_hover"]:
            x=self.view.messages["event"].x//self.view.messages["cell_size"]
            y=self.view.messages["event"].y//self.view.messages["cell_size"]
            if x >= self.view.messages["grid_max_x"]:
                x = self.view.messages["grid_max_x"]
            if x <= GRID_MIN:
                x = GRID_MIN
            if y >= self.view.messages["grid_max_y"]:
                y = self.view.messages["grid_max_y"]
            if y <= GRID_MIN:
                y = GRID_MIN
            self.view.messages["cursor_x"] = x
            self.view.messages["cursor_y"] = y
            self.update_cursor_position()
            self.display_layer_pixel(self.view.messages["hover_id"], self.px, self.py)
            self.px = x
            self.py = y
            self.update_cell(x,y,self.view.messages["tool_hover_color"])
            self.view.unset_pen_hover()
       
        if self.view.messages["tool_leave"]:
            self.display_layers(self.view.messages["hover_id"])
            self.view.unset_tool_leave()

#===================CHOOSING_TOOLS=======================================
        if self.view.messages["change_tool"]:
            self.view.grid.change_cursor(self.view.messages["tool_cursor"])
            if self.view.messages["tool"] == ERASER:
                self.view.grid.bind_eraser()
            if self.view.messages["tool"] == PEN:
                self.view.grid.bind_pen()
            if self.view.messages["tool"] == CIRCLE:
                self.view.grid.bind_circle()
            if self.view.messages["tool"] == SPRAY:
                self.view.grid.bind_spray()
            self.view.unset_change_tool()

#===================MENU_BAR==============================================
        if self.view.messages["new_project"]:
            self.init_new_project()

        if self.view.messages["create_new_project"]:
            if self.view.messages["new_project_width"].isdigit() and self.view.messages["new_project_height"].isdigit():
                width = int(self.view.messages["new_project_width"])
                height = int(self.view.messages["new_project_height"])
                if (width > 64):
                    mb.showinfo("","Maximum supported image size is 64px!")
                else:
                    self.view.messages["cells_x"] = width
                    self.view.messages["cells_y"] = height
                    #image size description under grid
                    self.view.grid.update_image_size()
                    #setting new project name
                    self.master.master.master.master.title(self.view.messages["new_project_name"])
                    self.view.messages["grid_max_x"] = width - 1
                    self.view.messages["grid_max_y"] = height - 1
                    self.clear_old_project()
                    self.create_new_project()
            self.view.unset_create_new_project()

        if self.view.messages["export"]:
            path = filedialog.asksaveasfilename(title = "Export")
            if path is not None and len(path) != 0:
                self.model.data.export_images(path)
                mb.showinfo("","Export successful!")
            self.view.unset_export()

        if self.view.messages["import_as_image"]:
            self.import_as_image()
            self.view.unset_import_as_image()

        if self.view.messages["import_as_layer"]:
            self.import_as_layer()
            self.view.unset_import_as_layer()

        if self.view.messages["open_project"]:
            self.open_project()
            self.view.unset_open_project()

        if self.view.messages["save_project"]:
            self.init_save_project()
            self.view.unset_save_project()

        if self.view.messages["exit"]:
            if (not mb.askyesno("Save project?", "Save project before closing?")):
                #project not daved before closing app
                exit()
            else:
                #project saved then app will close
                self.init_save_project()
                exit()
            self.view.unset_exit()

        if self.view.messages["show_help"]:
            content = "Shortcuts\nCtrl+i copy image\nCtrl+l copy layer\nCtrl+v paste image/layer"
            content += "\nInfo\nSupported image formats for import - PNG, JPEG, BMP\n"
            content += "Supported image formats for export - PNG"
            mb.showinfo("Shortcuts and Info", content)
            self.view.unset_show_help()
 
        self.master.after(10,self.controller_loop)
#######################################################################################
    
    def init_save_project(self, event = None):
        path = filedialog.asksaveasfilename(title = "Save project", initialfile = self.view.messages["new_project_name"])
        if path is not None and len(path) != 0:
            self.save_project(path)
    
    def init_new_project(self, event = None):
        self.view.new_project()
        self.view.unset_new_project()

    def update_main_picture(self,main_id,x,y,color):
        self.view.get_main(main_id).update_picture(x,y,color)

    def update_main_pixel(self, main_id, x, y, color):
        self.view.get_main(main_id).update_pixel(x,y,color)

    def update_part_picture(self,main_id,part_id,x,y,color):
        self.view.get_part(main_id,part_id).update_picture(x,y,color)

    def update_part_pixel(self,main_id,part_id,x,y,color):
        self.view.get_part(main_id,part_id).update_pixel(x,y,color)

    def update_data(self,main_id,part_id,x,y,color):
        self.model.data.data[main_id][part_id][x][y]=color

    def update_cell(self,x,y,color):
        self.view.grid.draw_cell(x,y,self.from_rgb(color))

    def update_cell_hexa(self, x, y, color):
        self.view.grid.draw_cell(x, y, color) 

    def update_view_model(self, x, y, color):
        self.update_cell(x,y,color)
        self.update_main_picture(self.view.messages["main_id"],x,y,color)
        self.update_part_picture(self.view.messages["main_id"],self.view.messages["part_id"],x,y,color)
        self.update_data(self.view.messages["main_id"],self.view.messages["part_id"],x,y,color)
        self.display_layer_pixel(self.view.messages["main_id"],x ,y)
    
    def from_rgb(self,rgb):
        #converts RGB color to HEXA color
        return "#%02x%02x%02x" % rgb  
    
    def erasing(self, main_id, x, y):
        if self.view.messages["tool"] == ERASER:
            self.display_layer_pixel(main_id, x, y)

    def on_release(self):
        self.old_x = False
        self.old_y = False

    def on_motion(self,event,color):
        cell_size = self.view.messages["cell_size"]
        if self.old_x and self.old_y:
            self.bressenham_line(self.old_x//cell_size, self.old_y//cell_size, event.x//cell_size, event.y//cell_size, color)
        self.old_x=event.x
        self.old_y=event.y

    def bressenham_line(self,old_x,old_y,new_x,new_y, color):
        #checking for out of bounds cursor position
        #x axis
        if old_x >= self.view.messages["grid_max_x"]:
            old_x = self.view.messages["grid_max_x"]
        if old_x <= GRID_MIN:
            old_x = GRID_MIN
        if new_x >= self.view.messages["grid_max_x"]:
            new_x = self.view.messages["grid_max_x"]
        if new_x <= GRID_MIN:
            new_x = GRID_MIN
        #y axis
        if old_y >= self.view.messages["grid_max_y"]:
            old_y = self.view.messages["grid_max_y"]
        if old_y <= GRID_MIN:
            old_y = GRID_MIN
        if new_y >= self.view.messages["grid_max_y"]:
            new_y = self.view.messages["grid_max_y"]
        if new_y <= GRID_MIN:
            new_y = GRID_MIN

        self.view.messages["cursor_x"] = old_x
        self.view.messages["cursor_y"] = old_y
        self.update_cursor_position()
       
        if (old_x!=new_x) or (old_y!=new_y):
            d_x=abs(new_x-old_x)
            d_y=abs(new_y-old_y)
            d=d_x-d_y
            p_x=0
            p_y=0
            p=0
            if old_x<new_x:
                p_x=1
            else:
                p_x=-1
            if old_y < new_y:
                p_y=1
            else:
                p_y=-1
            while (old_x != new_x) or (old_y!=new_y):
                p=2*d
                if (p>-d_y):
                    d-=d_y
                    old_x+=p_x
                if (p<d_x):
                    d+=d_x
                    old_y+=p_y
                self.update_view_model(old_x, old_y, color)
                #if pixel from top layer is removed, coresponding pixel is redrawn, so bottom layers are visible
                self.erasing(self.view.messages["main_id"], old_x, old_y)
    
    def bressenham_circle(self, xc, yc, r, color): 
        x = 0 
        y = r 
        d = 3 - 2 * r 

        self.circle(xc, yc, x, y, color); 
        while (y >= x):
            x += 1 
            if (d > 0): 
                y -= 1  
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6 
            self.circle(xc, yc, x, y, color)

    def update_cursor_position(self):
        self.view.grid.update_cursor()   

    def import_as_image(self, event = None):
        path = filedialog.askopenfilename(title = "Import", filetypes = [("PNG picture", ".png"),("JPG picture", ".jpg"),("BMP Picture", ".bmp")])
        if path is not None and len(path) != 0:
            try:
                image = Image.open(path)
            except:
                mb.showinfo("Pixelart", "Importing image failed!")
                return
            resized = image.resize((self.view.messages["cells_x"],self.view.messages["cells_y"]))
            pixels = resized.load()
            self.add_main()
            main = self.view.get_main(self.view.panel.board.get_current_main_id())
            part = self.view.get_main(self.view.panel.board.get_current_main_id()).parts[self.view.panel.board.get_current_part_id()] 
            for i in range(self.view.messages["cells_y"]):
                for j in range(self.view.messages["cells_x"]):
                    color = pixels[j, i]
                    if color == (0, 0, 0, 0):
                        color = TRANSPARENT_COLOR_RGBA
                    main.update_pixel(j, i, color)
                    part.update_pixel(j, i, color)
                    self.model.data.update_pixel(self.view.panel.board.get_current_main_id(),self.view.panel.board.get_current_part_id(), j, i, color[0:3])
                    self.view.grid.draw_cell(j, i, self.from_rgb(color[0:3]))
            main.create_picture()
            main.set_picture()
            part.create_picture()
            part.set_picture()

    def import_as_layer(self):
        path = filedialog.askopenfilename(title = "Import", filetypes = [("PNG picture", ".png"),("JPG picture", ".jpg"),("BMP Picture", ".bmp")])
        if path is not None and len(path) != 0:
            try:
                image = Image.open(path)
            except:
                mb.showinfo("Pixelart", "Importing layer failed!")
                return
            resized = image.resize((self.view.messages["cells_x"],self.view.messages["cells_y"]))
            pixels = resized.load()
            if self.view.messages["hover_id"] is not None:
                self.view.messages["main_id"] = self.view.panel.board.get_current_main_id()
                self.add_part()
                part = self.view.get_main(self.view.panel.board.get_current_main_id()).parts[self.view.panel.board.get_current_part_id()] 
                for i in range(self.view.messages["cells_y"]):
                    for j in range(self.view.messages["cells_x"]):
                        color = pixels[j, i]
                        if color == (0, 0, 0, 0):
                            color = TRANSPARENT_COLOR_RGBA
                        self.model.data.update_pixel(self.view.panel.board.get_current_main_id(),self.view.panel.board.get_current_part_id(), j, i, color[0:3])
                        self.display_layer_pixel(self.view.messages["hover_id"], j, i)
                        part.update_pixel(j, i, color)
                part.create_picture()
                part.set_picture()
