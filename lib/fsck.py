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

    def __init__(self, side: Side, displaycontroller: DisplayController):
        self.side = side
        self.displaycontroller = displaycontroller

        self.cells = []

        self.color = (255, 255, 0)
        for y, row in enumerate(fsck_banner):
            for x, pixel_value in enumerate(row):
                if pixel_value == 1:
                    c = CellPos(side, x, MATRIX_SIZE - y - 1)
                    self.cells.append(c)
                

    def update(self):
        self.displaycontroller.clearMatrix()

        for c in self.cells:
            try:
                c.move(Direction.RIGHT)
            except:
                c.side = self.side
                c.x = 0
            self.displaycontroller.writePixel(c, self.color)
        self.displaycontroller.updateMatrix()
            
