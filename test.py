from machine import Pin, Timer#, ADC
from neopixel import NeoPixel
from timeE import sleep_ms
#import webserver
from random import randrange
from lib.cell_pos import CellPos
from lib.side import Side
from lib.enums import Direction
from lib.mapper import Mapper
#from lib.nunchuck import Nunchuck
import _thread

MATRIX_SIZE = 15

class DisplayController:
    
    def __init__(self):
        self.mapper = Mapper(MATRIX_SIZE)
        self.topright_pixels = NeoPixel(Pin(16, Pin.OUT), MATRIX_SIZE * MATRIX_SIZE * 2)
        self.leftfront_pixels = NeoPixel(Pin(17, Pin.OUT), MATRIX_SIZE * MATRIX_SIZE * 2)
    
    def updateMatrix(self):
        self.topright_pixels.write()
        self.leftfront_pixels.write()
    
    def writePixel(self, side: str, x: int, y: int, color):
        pixelIndex = self.mapper.pos_to_pixel(side, x, y)
        
        if 0 == pixelIndex[0]:
            self.leftfront_pixels[pixelIndex[1]] = color
        elif 1 == pixelIndex[0]:
            self.topright_pixels[pixelIndex[1]] = color
                
    def fullColor(self, r, g, b):
        self.clearMatrix()
        self.updateMatrix()
        for i in range(0, MATRIX_SIZE * MATRIX_SIZE * 2): self.topright_pixels[i] = (r, g, b)
        for i in range(0, MATRIX_SIZE * MATRIX_SIZE * 2): self.leftfront_pixels[i] = (r, g, b)
        self.updateMatrix()
        sleep_ms(500)
        self.clearMatrix()
        self.updateMatrix()
        
    def clearMatrix(self):
        for m in [self.leftfront_pixels, self.topright_pixels]: m.fill((0, 0, 0))

if __name__ == "__main__":
    d = DisplayController()
    
    front = Side("front", MATRIX_SIZE)
    top = Side("top", MATRIX_SIZE)
    left = Side("left", MATRIX_SIZE)
    right = Side("right", MATRIX_SIZE)

    front.attach_top(top, Direction.DOWN)
    front.attach_left(left, Direction.RIGHT)
    front.attach_right(right, Direction.LEFT)

    top.attach_down(front, Direction.UP)
    top.attach_left(left, Direction.UP)
    top.attach_right(right, Direction.UP)

    left.attach_right(front, Direction.LEFT)
    left.attach_top(top, Direction.LEFT)

    right.attach_left(front, Direction.RIGHT)
    right.attach_top(top, Direction.RIGHT)
    
    sides = [front, top, left, right]

    pixles = [CellPos(front, x, 14) for x in range(15)]

    while True:
        for pixel in pixles:
            pixel.move(Direction.LEFT)
            d.writePixel(pixel.side.name, pixel.x, pixel.y, (0, 0, 255))
        
        d.updateMatrix()
        sleep_ms(200)
        d.clearMatrix()

