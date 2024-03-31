from machine import Pin
from neopixel import NeoPixel

Pin()
n = NeoPixel(0, 15 * 15 * 2)
n[3] = (0, 255, 0)
n.show()