from tkinter import *
import cell as cl
from config import *
import math

class Grid(Canvas):

    def __init__(self, master = None, panel = None, messages = None, **kwargs):
        self.options = {"master":master, **kwargs}
        super().__init__(**self.options)
        self.place(x = GRID_INIT_PX, y = GRID_INIT_PY, width = GRID_INIT_WIDTH, height = GRID_INIT_HEIGHT)
        self.cell_size = CELL_INIT_SIZE
        self.messages = messages
        self.panel = panel
        self.create_widgets()
        self.bind_buttons()
        self.cells = []
        self.create_cells()
        #after app start default tool is pen
        self.bind_pen()
        self.px = PX_INIT
        self.py = PY_INIT

    def create_widgets(self):
        #centering canvas, if its size is smaller then grid frame
        self.update_px(CANVAS_INIT_WIDTH)
        self.update_py(CANVAS_INIT_HEIGHT)
        #scrollable frame
        self.scrollable_frame = LabelFrame(master = self, bg = GRID_INIT_BACKGROUND_COLOR, width = CANVAS_INIT_WIDTH, height = CANVAS_INIT_HEIGHT, bd = 0, highlightthickness = 0)
        #canvas
        self.canvas = Canvas(master = self.scrollable_frame, bg = GRID_INIT_BACKGROUND_COLOR, cursor = "pencil", bd = 0, width = CANVAS_INIT_WIDTH, height = CANVAS_INIT_HEIGHT, highlightthickness = 0)
        self.canvas.place(x = CANVAS_INIT_PX, y = CANVAS_INIT_PY, width = CANVAS_INIT_WIDTH, height = CANVAS_INIT_HEIGHT)
        self.create_window((self.px, self.py),window=self.scrollable_frame,anchor="nw")
        #X_scrollbar
        self.scrollbar_x=Scrollbar(master=self.master,orient=HORIZONTAL)
        self.scrollbar_x.config(command=self.xview)
        self.scrollbar_x.place(x = SCROLLBAR_X_PX, y = SCROLLBAR_X_PY, width = SCROLLBAR_X_WIDTH, height = SCROLLBAR_X_HEIGHT)
        self.config(xscrollcommand=self.scrollbar_x.set)
        #Y_scrollbar
        self.scrollbar_y=Scrollbar(master=self. master,orient=VERTICAL)
        self.scrollbar_y.config(command=self.yview)
        self.scrollbar_y.place(x = SCROLLBAR_Y_PX, y = SCROLLBAR_Y_PY, width = SCROLLBAR_Y_WIDTH, height = SCROLLBAR_Y_HEIGHT)
        self.config(yscrollcommand=self.scrollbar_y.set)
        #binding trigger whenever scrollbar size changes (main is added or removed)
        self.scrollable_frame.bind("<Configure>",lambda e: self.configure(scrollregion=self.bbox(ALL)))
        #grid info + mouse position
        self.image_size_var = StringVar(value = "Image size: " + str(self.messages["cells_x"]) + "x" + str(self.messages["cells_y"]) + " px")
        self.image_size = Label(master = self.master, textvariable = self.image_size_var, bg = "white" )
        self.image_size.place(x = 611, y = 629, width = 180, height = 25)
        self.cursor_label_var = StringVar(value = "Cursor position:")
        self.cursor_label = Label(master = self.master, textvariable = self.cursor_label_var, bg = "white")
        self.cursor_label.place(x = 796, y = 629, width = 120, height = 25)
        self.cursor_position_var = StringVar(value = str(self.messages["cursor_x"]) + ", " + str(self.messages["cursor_y"]))
        self.cursor_position = Label(master = self.master, textvariable = self.cursor_position_var, bg = "white")
        self.cursor_position.place(x = 916, y = 629, width = 60, height = 25)

    def bind_buttons(self):
        #zooming eanbled when cursor hovering grid
        self.bind("<Control-Button-4>",self.mouse_wheel_up)
        self.bind("<Control-Button-5>",self.mouse_wheel_down)
        #zooming enabled when cursor hovering canvas
        self.canvas.bind("<Control-Button-4>",self.mouse_wheel_up)
        self.canvas.bind("<Control-Button-5>",self.mouse_wheel_down)
        #moving canvas with arrow
        self.focus_set()
        self.bind("<Left>",  lambda event: self.xview_scroll(-1, "units"))
        self.bind("<Right>", lambda event: self.xview_scroll( 1, "units"))
        self.bind("<Up>",    lambda event: self.yview_scroll(-1, "units"))
        self.bind("<Down>",  lambda event: self.yview_scroll( 1, "units"))

    def mouse_wheel_up(self,event):
        change = True
        self.cell_size += ZOOM_IN
        if self.cell_size >= MAX_ZOOM:
            self.cell_size = MAX_ZOOM
            change = False
        if change:
            self.update_canvas_size()
        
    def mouse_wheel_down(self,event):
        change = True
        self.cell_size += ZOOM_OUT
        if self.cell_size <= MIN_ZOOM:
            self.cell_size = MIN_ZOOM
            change = False
        if change == True:
            self.update_canvas_size()

    #FOR DRAWING AND ERASING ARE BEING USED SAME METHODS (draw_single(), draw_multiple()) !!!
    #IN CONTROLLER LOOP IS CHEKING FOR ERASING, SO LAYER ARE BEING REDRAWN !!! 
    def bind_pen(self):
        #left mouse button
        self.canvas.bind("<Button-1>",self.set_draw_single_left)
        self.canvas.bind("<B1-Motion>",self.set_draw_multiple_left)
        self.canvas.bind("<ButtonRelease-1>",self.set_draw_release)

        #right mouse button
        self.canvas.bind("<Button-3>",self.set_draw_single_right)
        self.canvas.bind("<B3-Motion>",self.set_draw_multiple_right)
        self.canvas.bind("<ButtonRelease-3>",self.set_draw_release)

        self.canvas.bind("<Motion>",self.set_pen_hover)
        self.canvas.bind("<Leave>", self.set_tool_leave)

    def bind_eraser(self):
        #binding left mouse button
        self.canvas.bind("<Button-1>",self.set_draw_single_left)
        self.canvas.bind("<B1-Motion>",self.set_draw_multiple_left)
        self.canvas.bind("<ButtonRelease-1>",self.set_draw_release)
        self.unbind_right_motion()
        self.canvas.unbind("<Button-3>")

    def bind_spray(self):
        self.canvas.bind("<Button-1>",self.set_left_spray)
        self.canvas.bind("<Button-3>",self.set_right_spray)
        #no mouse motion in spray
        self.unbind_left_motion()
        self.unbind_right_motion()

    def bind_circle(self):
        self.canvas.bind("<Button-1>", self.set_left_circle)
        self.canvas.bind("<Button-3>", self.set_right_circle)
        self.canvas.bind("<Motion>",self.set_circle_hover)
        self.canvas.bind("<Leave>", self.set_tool_leave)
        self.unbind_left_motion()
        self.unbind_right_motion()

    def set_draw_release(self,event):
        self.messages["draw_release"]=True

    def set_draw_multiple_left(self,event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_multiple"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = LEFT_BUTTON
            self.messages["event"]=event

    def set_draw_single_left(self,event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_single"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = LEFT_BUTTON
            self.messages["event"]=event

    def set_draw_multiple_right(self,event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_multiple"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = RIGHT_BUTTON
            self.messages["event"]=event

    def set_draw_single_right(self,event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_single"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = RIGHT_BUTTON
            #AFTER RIGHT CLICK, HOVER PEN COLOR CHANGES TO RIGHT CLICK COLOR
            self.messages["tool_hover_color"] = self.messages["colors"][RIGHT_BUTTON]
            self.messages["event"]=event

    def set_left_spray(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["spray"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = LEFT_BUTTON

    def set_right_spray(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["spray"]=True
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = RIGHT_BUTTON
            #AFTER RIGHT CLICK, HOVER PEN COLOR CHANGES TO RIGHT CLICK COLOR
            self.messages["tool_hover_color"] = self.messages["colors"][RIGHT_BUTTON]


    def set_pen_hover(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["pen_hover"] = True
            self.messages["hover_id"] = self.panel.board.get_current_main_id()
            self.messages["event"] = event
            #init hover color is left button color
            self.messages["tool_hover_color"] = self.messages["colors"][LEFT_BUTTON]

    def set_left_circle(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_circle"] = True
            self.messages["event"] = event
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = LEFT_BUTTON

    def set_right_circle(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["draw_circle"] = True
            self.messages["event"] = event
            self.messages["main_id"]=self.panel.board.get_current_main_id()
            self.messages["hover_id"]=self.panel.board.get_current_main_id()
            self.messages["part_id"]=self.panel.board.get_current_part_id()
            self.messages["which_button"] = RIGHT_BUTTON

    def set_circle_hover(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["circle_hover"] = True
            self.messages["hover_id"] = self.panel.board.get_current_main_id()
            self.messages["event"] = event
            #init hover color is left button color
            self.messages["tool_hover_color"] = self.messages["colors"][LEFT_BUTTON]

    def set_tool_leave(self, event):
        if self.messages["drawing_enabled"]:
            self.messages["tool_leave"] = True
            self.messages["hover_id"] = self.panel.board.get_current_main_id()
            self.messages["event"] = event

    def create_cells(self,size = CELL_INIT_SIZE):
        for i in range(self.messages["cells_y"]):
            self.cells.append([])
            for j in range(self.messages["cells_x"]):
                self.cells[i].append(cl.Cell(size = size))
                self.cells[i][j].set_location(i * size + 1,j*size + 1)
                self.cells[i][j].render(self.canvas)

    def draw_cell(self,x,y,color):
        self.set_color(x,y,color)
        self.render_cell(x,y)

    def clear_cells(self):
        self.cells.clear()

    def render_cell(self,x,y):
        self.cells[x][y].render(self.canvas)

    def reset_cell(self,x,y):
        self.cells[x][y].color=TRANSPARENT_COLOR_HEXA

    def set_color(self,x,y,color):
        self.cells[x][y].color=color

    def set_size(self,x,y,size):
        self.cells[x][y].size = size

    def set_location(self,x,y):
        self.place(x=x,y=y,width=self.options["width"],height=self.options["height"])

    def clear_grid(self):
        for i in range(self.messages["cells_y"]):
            for j in range(self.messages["cells_x"]):
                self.draw_cell(j,i,TRANSPARENT_COLOR_HEXA)

    def clear_canvas(self):
        self.canvas.delete("all")

    def change_cursor(self, new_cursor):
        self.canvas.config(cursor = new_cursor)

    def delete_cell(self, x, y):
        self.canvas.delete(self.cells[x][y])

    def unbind_left_motion(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def unbind_right_motion(self):
        self.canvas.unbind("<B3-Motion>")
        self.canvas.unbind("<ButtonRelease-3>")

    def resize_and_redraw(self, size):
        for i in range(self.messages["cells_y"]):
            for j in range(self.messages["cells_x"]):
                self.cells[i][j].set_location(i * size + 1, j * size + 1)
                self.cells[i][j].set_size(size)
                self.cells[i][j].render(self.canvas)

    def update_px(self, canvas_width):
        self.px = (GRID_INIT_WIDTH - canvas_width) // 2

    def update_py(self, canvas_height):
        self.py = (GRID_INIT_HEIGHT - canvas_height) // 2

    def update_canvas_size(self):
        self.messages["cell_size"] = self.cell_size
        new_width = self.cell_size * self.messages["cells_x"] + 3
        new_height = self.cell_size * self.messages["cells_y"] + 3
        self.update_px(new_width)
        self.update_py(new_height)
        self.scrollable_frame.config(width = new_width, height = new_height)
        self.canvas.place(x = 0, y = 0, width = new_width, height = new_height)
        self.create_window((self.px, self.py),window=self.scrollable_frame,anchor="nw")
        self.canvas.delete(ALL)
        self.resize_and_redraw(self.cell_size)

    def update_cursor(self):
        self.cursor_position_var.set(str(self.messages["cursor_x"]) + ", " + str(self.messages["cursor_y"]))

    def reset_cell_size(self):
        self.cell_size = CELL_INIT_SIZE

    def update_image_size(self):
        self.image_size_var = StringVar(value = "image size: " + str(self.messages["cells_x"]) + "x" + str(self.messages["cells_y"]) + " px")
        self.image_size["textvariable"]= self.image_size_var

