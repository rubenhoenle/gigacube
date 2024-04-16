from machine import Pin, Timer
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

speed = 200

class Player:


    def __init__(self, side, sides, color):

        self.area = set() # aquierd space
        self.trail = [] # trail of player
        self.sides = sides

        self.hit = False

        self.headColor = color
        self.areaColor = (int(color[0]/2), int(color[1]/2), int(color[2]/2))
        self.trailColor = (int(color[0]/3), int(color[1]/3), int(color[2]/3))

        start_x, start_y = 7, 7
        self.head = CellPos(side, start_x, start_y)

        for x in range(-1, 2):
            for y in range(-1 ,2):
                self.area.add(CellPos(side, start_x + x, start_y + y))

        self.direction = Direction.UP

    def moveLeft(self):
        if self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        
    def moveRight(self):
        if self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
                    
    def moveUp(self):
        if self.direction != Direction.DOWN:
            self.direction = Direction.UP
        
    def moveDown(self):
        if self.direction != Direction.UP:
            self.direction = Direction.DOWN
    
    def calculateNewArea(self):
        sidesNeeded = {punkt.side for punkt in self.trail}
        visited = set()
        area = self.area  # Cache object reference
        trail = self.trail  # Cache object reference
        for side in sidesNeeded:
            for x in range(MATRIX_SIZE):
                for y in range(MATRIX_SIZE):
                    if (side, x, y) in visited or CellPos(side, x, y) in area:  # Use cached object reference
                        continue
                    ups, downs, lefts, rights = self.checkHitInAllDirections(side, x, y, visited)
                    if ups and downs and lefts and rights:
                        cells_to_update = ups | downs | lefts | rights
                        area.update(cells_to_update)  # Use cached object reference
                        visited.update(cells_to_update)
        area.update(trail)  # Use cached object reference
        trail.clear()  # Use cached object reference

    def checkHitInAllDirections(self, side, x, y, visited):
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        hits = {direction: self.checkHitInDirection(direction, side, x, y, visited) for direction in directions}
        return hits[Direction.UP], hits[Direction.DOWN], hits[Direction.LEFT], hits[Direction.RIGHT]

    def checkHitInDirection(self, direction: Direction, side, x, y, visited) -> set:
        sleep_ms(10)
        c = CellPos(side, x, y)
        area = set()
        while True:
            if c in self.area or c in self.trail:
                return area
            if (side, x, y) in visited:
                return set()
            area.add(c.clone())
            try:
                c.move(direction)
            except ValueError:
                return set()



    def update(self) -> bool:
        self.direction = self.head.move(self.direction)

        if self.head not in self.area:
            self.trail.append(self.head.clone())

        if self.head in self.area and len(self.trail) > 0:
            return True

        return False



class Snake:

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

    display_controller = DisplayController()

    players = []


    
    def updatePlayers(self):
        """updadates all players head, area and trail. Checks for collision and out of bounce"""
        toRemove = [] # so that players can hit each ohter at the same time

        for player in self.players:
            
            try:
                if player.update(): # true when area is sourunded -> player hit area again and trail > 0
                    self.calc(player)
            except ValueError:
                toRemove.append(player) # out of bounce

            for area in player.area:
                self.display_controller.writePixel(area, player.areaColor)

        for player in self.players:
            
            for otherPlayer in self.players:
                if player != otherPlayer:
                    if player.head in otherPlayer.trail:
                        toRemove.append(otherPlayer)

            for trail in player.trail:
                self.display_controller.writePixel(trail, player.trailColor)

            self.display_controller.writePixel(player.head, player.headColor)

        for remove in toRemove:
            self.players.remove(remove)


    def calc(self, player):
        """calcualates new area for player and removes area from others"""

        player.calculateNewArea()

        for otherPlayer in self.players:
            if player != otherPlayer:
                otherPlayer.area = otherPlayer.area.difference(player.area)

    def tick(self, timer):
        """main game tick loop"""
        self.display_controller.clearMatrix()
        
        self.updatePlayers()
        
        if len(self.players) == 0:
            self.gameOver(timer)
        
        self.display_controller.updateMatrix()
        
    def gameOver(self, timer):
        """game over when no player is left"""
        timer.deinit()
        self.players = []
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(500)
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(500)
        self.display_controller.fullColor(255, 0, 0)
        sleep_ms(500)
        self.display_controller.clearMatrix()
        self.display_controller.updateMatrix()

    def startGame(self):
        """"starts game with players"""
        self.players = [ Player(self.left, self.sides, (0, 100, 255)) ]
        timer = Timer(-1)
        timer.init(period=speed, mode=Timer.PERIODIC, callback=self.tick)


i2c = machine.I2C(
        0, scl=machine.Pin(5),
        sda=machine.Pin(4),
        freq=100000)
sleep_ms(100)
nun = Nunchuck(i2c)

#sleep_ms(500)
def nunchuck_update(nunchuck: Nunchuck, player_id: int, gamelogic):

    if len(gamelogic.players) <= player_id:
        if len(gamelogic.players) == 0: # needed because lag in threads
            sleep_ms(10) 
        return

    sleep_ms(1000)

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
    if((b[0] or b[1]) and len(gamelogic.players) == 0): # condition seems to be true for some seconds after the start of the game
        gamelogic.startGame()

if __name__ == "__main__":
    snake = Snake()
    snake.startGame()

    while True:
        nunchuck_update(nun, 0, snake)
        nunchuck_update(nun, 1, snake)