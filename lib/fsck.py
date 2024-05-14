from machine import *
import machine
from neopixel import NeoPixel
from time import sleep_ms
#import webserver
from random import randrange
from .cell_pos import CellPos
from .side import Side
from .enums import Direction
from .mapper import Mapper
from .nunchuck import Nunchuck
from .displaycontroller import DisplayController, MATRIX_SIZE
import _thread

fsck_banner = [

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [1, 1, 1, 0, 1, 1, 0, 0, 1, 1 ,0 ,1 ,0 ,0 ,1],
        [1, 0, 0, 0, 1, 0, 0, 1, 0, 0 ,0 ,1 ,0 ,1 ,0],
        [1, 1, 0, 0, 1, 1, 0, 1, 0, 0 ,0 ,1 ,1 ,0 ,0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0 ,0 ,1 ,0 ,1 ,0],
        [1, 0, 0, 0, 1, 1, 0, 0, 1, 1 ,0 ,1 ,0 ,0 ,1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0],
        ]

class IdleScreen:

    colors = [
                [255, 0, 0],
                [0, 255, 0],
                [0, 0, 255],
                [255, 255, 0],
                [255, 255, 0],
                [0, 255, 255],
            ]

    def __init__(self, side: Side, displaycontroller: DisplayController):
        self.side = side
        self.displaycontroller = displaycontroller

        self.cells = []

        for y, row in enumerate(fsck_banner):
            for x, pixel_value in enumerate(row):
                if pixel_value == 1:
                    c = CellPos(side, x, MATRIX_SIZE - y - 1)
                    self.cells.append([c, 0]) 
                

    def update(self):
        self.displaycontroller.clearMatrix()

        for index, c_data in enumerate(self.cells):

            c, color_index = c_data

            try:
                c.move(Direction.RIGHT)
            except:
                c.side = self.side
                c.x = 0
                
                new_index = color_index +1
                if new_index >= len(self.colors):
                    new_index = 0

                self.cells[index][1] = new_index

            self.displaycontroller.writePixel(c, self.colors[color_index])
        self.displaycontroller.updateMatrix()
            
