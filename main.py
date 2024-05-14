from machine import *
import machine
from neopixel import NeoPixel
from time import sleep_ms
#import webserver
from random import randrange
from lib.cell_pos import CellPos
from lib.side import Side
from lib.enums import Direction
from lib.mapper import Mapper
from lib.nunchuck import Nunchuck
from lib.displaycontroller import DisplayController, MATRIX_SIZE
import _thread
from lib.fsck import IdleScreen

speed = 200

class Player:
    def __init__(self, pos, direction, player_id, snake_color):
        self.pos = pos
        self.player_id = player_id
        self.direction = direction
        self.body = []
        self.snake_color = snake_color
        self.previous_pos = self.pos
        self.body_color = snake_color.copy()
        self.body_color[2] = 10
        self.alive = True

    def move(self):
        self.previous_pos = self.pos.clone()
        d = -1
        
        if self.direction == "left": d = Direction.LEFT # TODO use Direction in Gamelogic
        elif self.direction == "right": d = Direction.RIGHT
        elif self.direction == "up": d = Direction.UP
        elif self.direction == "down": d = Direction.DOWN
        
        d = self.pos.move(d)
        
        if d == Direction.LEFT: self.direction = "left"
        elif d == Direction.RIGHT: self.direction =  "right"
        elif d == Direction.UP: self.direction = "up"
        elif d == Direction.DOWN: self.direction = "down"
            
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
            if self.pos == b: raise ValueError("player hit themself")
        
    def addLength(self):
        if len(self.body) == 0:
            self.body.append(self.previous_pos)
        else:
            self.body.append(self.body[-1])
        
    def getSnakePixels(self):
        pass

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
    
    idle = False

    cookie_color = (10, 10, 10)

    players = [
        #Player(0, 0, 1),
        #Player(CellPos(front, 0, 0), "up", 2)
    ]
    cookies = []#[(0,1),(0,2),(0,3),(0,4),(0,5)]
    display_controller = DisplayController()
    
    #def __init__(self):
    #    self.generateCookies()
    
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
        while len(self.cookies) < 40:
            i = randrange(len(self.sides))
            self.cookies.append(CellPos(self.sides[i], randrange(MATRIX_SIZE-1),randrange(MATRIX_SIZE-1)))
    
    def movePlayers(self):
        for player in self.players:
            if not player.alive:
                continue
            try:
                player.move()
            except ValueError:
                player.alive = False
                continue
            
            for other in self.players:
                if player == other:
                    continue

                if player.pos in other.body:
                    player.alive = False

            self.checkCookies()
            player.moveBody()

    def writePlayerPosToMatrix(self):
        for player in self.players:
            if not player.alive:
                continue

            self.display_controller.writePixel(player.pos, player.snake_color)
            for b in player.body:
                self.display_controller.writePixel(b, player.body_color)
            
    def writeCookiesToMatrix(self):
        for cookie in self.cookies:
            self.display_controller.writePixel(cookie, self.cookie_color)
            
    def tick(self, timer):
        self.display_controller.clearMatrix()
        
        self.movePlayers()
        
        self.writePlayerPosToMatrix()
        self.writeCookiesToMatrix()
        self.display_controller.updateMatrix()

        still_alive = 0
        last_one = None # if only one left this is the one

        for player in self.players:
            if player.alive:
                still_alive += 1
                last_one = player

        if still_alive == 1:
            self.win_animation(timer, last_one)
        elif still_alive == 0:
            self.gameOver(timer)
    
    def win_animation(self, timer, player: Player):
        timer.deinit()
        self.display_controller.fullColor(player.snake_color[0], player.snake_color[1], player.snake_color[2])
        sleep_ms(200)
        self.display_controller.fullColor(player.snake_color[0], player.snake_color[1], player.snake_color[2])
        self.idle = True
        self.payers = []
        self.display_controller.clearMatrix()
        self.display_controller.updateMatrix()

    def gameOver(self, timer):
        timer.deinit()
        self.players = []
        self.cookies = []
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(200)
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(200)
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(200)
        self.display_controller.clearMatrix()
        self.display_controller.updateMatrix()
        self.idle = True

    def startGame(self):
        # restart the game

        first_player = [0, 0, 255]
        second_player = [100, 100, 0]

        self.players = [Player(CellPos(self.right, 7, 0), "up", 2, first_player), Player(CellPos(self.left, 7, 0), "up", 3, second_player)]

        #self.cookies = [(0,1),(0,2),(0,3),(0,4),(0,5)]
        self.cookies = []
        self.generateCookies()
        self.idle = False
        self.display_controller.clearMatrix()
        self.display_controller.fullColor(0, 255, 0)
        self.display_controller.updateMatrix()
        sleep_ms(100)
        timer = Timer(-1)
        timer.init(period=speed, mode=Timer.PERIODIC, callback=gamelogic.tick)

gamelogic = GameLogic()

gamelogic.startGame()

i2c = machine.I2C(
        1, scl=machine.Pin(7),
        sda=machine.Pin(6),
       freq=100000)

sleep_ms(100)

i2c2 = machine.I2C(
        0, scl=machine.Pin(5),
        sda=machine.Pin(4),
        freq=100000)
sleep_ms(100)

nun = Nunchuck(i2c)
sleep_ms(100)
nun2 = Nunchuck(i2c2)

def nunchuck_update(nunchuck: Nunchuck, player_id: int, gamelogic: GameLogic):
    if not nunchuck.joystick_center() and len(gamelogic.players) > 0:
        if nunchuck.joystick_up():
            gamelogic.players[player_id].moveUp()
        elif nunchuck.joystick_down():
            gamelogic.players[player_id].moveDown()
        elif nunchuck.joystick_left():
            gamelogic.players[player_id].moveLeft()
        elif nunchuck.joystick_right():
            gamelogic.players[player_id].moveRight()

    
    b = nunchuck.buttons()
    if((b[0] or b[1]) and gamelogic.idle): # condition seems to be true for some seconds after the start of the game
        gamelogic.startGame()

idlescreen = IdleScreen(gamelogic.left, gamelogic.display_controller)

while True:
    nunchuck_update(nun, 1, gamelogic)
    nunchuck_update(nun2, 0, gamelogic)
    if gamelogic.idle:
        idlescreen.update()
        sleep_ms(100)
        
