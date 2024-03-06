from machine import Pin, Timer, ADC
from neopixel import NeoPixel
from time import sleep_ms
#import webserver
from random import randrange
from lib.cell_pos import CellPos
from lib.side import Side
from lib.enums import Direction
from lib.mapper import Mapper
from lib.nunchuck import Nunchuck

MATRIX_SIZE = 15
speed = 200

class Player:
    
    def __init__(self, pos, direction, player_id):
        self.pos = pos
        self.player_id = player_id
        self.direction = direction
        self.body = []
        self.previous_pos = self.pos
        
    def move(self):
        self.previous_pos = self.pos.clone()
        d = -1
        if self.direction == "left": d = Direction.LEFT
        elif self.direction == "right": d = Direction.RIGHT
        elif self.direction == "up": d = Direction.UP
        elif self.direction == "down": d = Direction.DOWN
        
        if not self.pos.move(d):
            raise ValueError('player went out of matrix')
            
    def moveLeft(self):
        if self.direction != "right":
            self.direction = "left"
        
    def moveRight(self):
        if self.direction != "left":
            self.direction = "right"
        
    def moveUp(self):
        if self.direction != "down":
            self.direction = "up"
        
    def moveDown(self):
        if self.direction != "up":
            self.direction = "down"
        
    def moveBody(self):
        if len(self.body) > 0:
            self.body.insert(0, self.previous_pos)
            self.body.pop()
        for b in self.body:
            if self.pos.x == b.x and self.pos.y == b.y: raise ValueError('player bite itself')
        
    def addLength(self):
        if len(self.body) == 0:
            self.body.append(self.previous_pos)
        else:
            self.body.append(self.body[-1])
        
    def getSnakePixels(self):
        pass

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
        
        brightness = 10
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
        
class GameLogic:
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
    
    snake_color = (0, 200, 0)
    cookie_color = (20, 20, 20)

    players = [
        #Player(0, 0, 1),
        Player(CellPos(front, 0, 0), "up", 2)
    ]
    cookies = []#[(0,1),(0,2),(0,3),(0,4),(0,5)]
    display_controller = DisplayController()
    
    def __init__(self):
        self.generateCookies()
    
    def checkCookies(self):
        for cookie in self.cookies:
            for player in self.players:
                pass
                if cookie.x == player.pos.x and cookie.y == player.pos.y:
                    # self.display_controller.fullColor(0, 22, 0)
                    player.addLength()
                    self.cookies.remove(cookie)
        self.generateCookies()
                    
    def generateCookies(self):
        while len(self.cookies) < 6:
            i = randrange(len(self.sides))
            self.cookies.append(CellPos(self.sides[i], randrange(MATRIX_SIZE-1),randrange(MATRIX_SIZE-1)))
    
    def movePlayers(self):
        for player in self.players:
            player.move()
            self.checkCookies()
            player.moveBody()
        
    def writePlayerPosToMatrix(self):
        for player in self.players:
            self.display_controller.writePixel(player.pos.side.name, player.pos.x, player.pos.y, self.snake_color)
            for b in player.body:
                self.display_controller.writePixel(b.side.name, b.x, b.y, self.snake_color)
            
    def writeCookiesToMatrix(self):
        for cookie in self.cookies:
            self.display_controller.writePixel(cookie.side.name, cookie.x, cookie.y, self.cookie_color)
            
    def tick(self, timer):
        self.display_controller.clearMatrix()
        try:
            self.movePlayers()
        except ValueError:
            self.gameOver(timer)
        self.writePlayerPosToMatrix()
        self.writeCookiesToMatrix()
        self.display_controller.updateMatrix()
        
    def gameOver(self, timer):
        timer.deinit()
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(500)
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(500)
        self.display_controller.fullColor(255, 0, 0)
        
        # restart the game
        self.players = [Player(CellPos(self.front, 0, 0), "up", 2)]
        #self.cookies = [(0,1),(0,2),(0,3),(0,4),(0,5)]
        timer.init(period=speed, mode=Timer.PERIODIC, callback=gamelogic.tick)

gamelogic = GameLogic()

timer = Timer(-1)
timer.init(period=speed, mode=Timer.PERIODIC, callback=gamelogic.tick)

# nunchuck control

i2c = machine.I2C(
        0, scl=machine.Pin(5),
        sda=machine.Pin(4),
        freq=100000)
sleep_ms(100)

nun = Nunchuck(i2c)

#sleep_ms(500)
x = 0
y = 0

while True:
    #webserver.webserver_hook(gamelogic)

    if not nun.joystick_center():
        if nun.joystick_up():
            y += 1
            gamelogic.players[0].moveUp()
        elif nun.joystick_down():
            y -= 1
            gamelogic.players[0].moveDown()
        if nun.joystick_left():
            x -= 1
            gamelogic.players[0].moveLeft()
        elif nun.joystick_right():
            x += 1
            gamelogic.players[0].moveRight()
    print(x, y, nun.joystick_x(), nun.joystick_y())

    j = nun.joystick()
    a = nun.accelerator()
    b = nun.buttons()
    print("Joystick: X={0: <3} Y={1: <3} Accelerator: X={2: <3} Y={3: <3} Z={4: <3} Buttons: C={5} Z={6}".format(
            j[0], j[1],
            a[0], a[1], a[2],
            b[0], b[1]
            ))

    sleep_ms(100)
    
