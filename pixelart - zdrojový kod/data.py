from config import *
import numpy as np
from PIL import Image

class Data():

    def __init__(self, messages):
        self.data={}
        self.keys=[]
        self.transparent_color=(254,254,254)
        self.messages = messages

    def add_image(self,main_id):
        self.data[main_id]={}
        self.keys.append(main_id)

    def add_layer(self,main_id,part_id):
        self.data[main_id][part_id]=[[self.transparent_color for i in range(self.messages["cells_y"])] for j in range(self.messages["cells_x"])]

    def get_color(self,main_id,part_id,x,y):
        return self.data[main_id][part_id][x][y]

    def clear(self):
        self.data.clear()
        self.keys.clear()
    
    def rotate_and_alpha(self, main_id):
        empty_img  = [[(0,0,0,0) for i in range(self.messages["cells_y"])] for j in range(self.messages["cells_x"])]
        for i in range(self.messages["cells_y"]):
            for j in range(self.messages["cells_x"]):
                for layer_id, layer in self.data[main_id].items():
                    if layer[j][i] != self.transparent_color:
                        empty_img[i][j] = layer[j][i] + (255,)
        return empty_img

    def update_pixel(self, main_id, part_id, x, y, color):
        self.data[main_id][part_id][x][y] = color
                    
    def export_images(self, path):
        index = 0
        for image_id in self.keys:
            array = self.rotate_and_alpha(image_id)
            img_array = np.array(array, dtype = np.uint8)
            new_image = Image.fromarray(img_array)
            try:
                new_image.save(path + str(index) + ".png", "PNG")
            except:
                print("Saving images failed!")
                return
            index += 1
