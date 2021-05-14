from tkinter import*
import panel_menu as pm
import board as bd
from config import *

class Panel(LabelFrame):

    def __init__(self, master = None, messages = None, **kwargs):
        self.options = {"master":master, **kwargs}
        super().__init__(**self.options)
        self.menu = pm.PanelMenu(master = self, messages = messages)
        self.board = bd.Board(master = self, messages = messages, **BOARD_INIT)
        self.place(x = PANEL_INIT_PX, y = PANEL_INIT_PY, width = PANEL_INIT_WIDTH, height = PANEL_INIT_HEIGHT)
        self.focus_set()

    def add_main(self):
        self.board.add_main()

    def get_board(self):
        return self.board
