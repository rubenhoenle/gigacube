from machine import Pin
from neopixel import NeoPixel
from timeE import sleep_ms
from .cell_pos import CellPos
from .mapper import Mapper

MATRIX_SIZE = 15

class DisplayController:
    
    def __init__(self):
        self.mapper = Mapper(MATRIX_SIZE)
        self.topright_pixels = NeoPixel(Pin(16, Pin.OUT), MATRIX_SIZE * MATRIX_SIZE * 2)
        self.leftfront_pixels = NeoPixel(Pin(17, Pin.OUT), MATRIX_SIZE * MATRIX_SIZE * 2)
    
    def updateMatrix(self):
        self.topright_pixels.write()
        self.leftfront_pixels.write()
    
    def writePixel(self, cell: CellPos, color):
        pixelIndex = self.mapper.pos_to_pixel(cell.side.name, cell.x, cell.y)
        
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
        
