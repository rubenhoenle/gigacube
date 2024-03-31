import threading
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Gigacube:


    sides = ["front", "top", "left", "right"]
    LED_MATRIX_SIZE = 15

    CUBE_POINTS = (
        (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
        (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
        (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5)
    )

    CUBE_COLORS = (
        (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
        (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
    )

    CUBE_QUAD_VERTS = (
        (3, 2, 7, 6), (6, 7, 5, 4), (1, 5, 7, 2), (4, 0, 3, 6), (4, 5, 1, 0)
    )

    CUBE_EDGES = (
        (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7),
    )

    def __init__(self):

        self.led_states = [[[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(self.LED_MATRIX_SIZE)] for _ in range(self.LED_MATRIX_SIZE)] for _ in range(4)]
        self.led_states_buff = [[[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(self.LED_MATRIX_SIZE)] for _ in range(self.LED_MATRIX_SIZE)] for _ in range(4)]
        print("in gigacube")
        thread = threading.Thread(target=self.main, args=())
        #thread.daemon = True                            # Daemonize thread
        thread.start() 


    def draw_led_matrix(self, led_matrix, pos, scale):
        offset = 1 / self.LED_MATRIX_SIZE / 2
        glBegin(GL_QUADS)
        for x in range(self.LED_MATRIX_SIZE):
            for y in range(self.LED_MATRIX_SIZE):
                for index, vert in enumerate((6, 7, 5, 4)):
                    pos = self.CUBE_POINTS[vert]
                    x_pos = (pos[0] * scale - 0.5 + x * (scale) + offset)
                    y_pos = pos[1] * scale + 0.5 - y * (scale) - offset

                    if index < 2:
                        x_pos += scale
                    else:
                        x_pos -= scale

                    if index == 0 or index == 3:
                        y_pos += scale
                    else:
                        y_pos -= scale

                    if led_matrix[y][x]:
                        glColor3f(led_matrix[y][x][0] / 255, led_matrix[y][x][1] / 255, led_matrix[y][x][2] / 255)
                        glVertex3f(x_pos, y_pos, pos[2] + 0.01)
        glEnd()

    def drawcube(self):
        glBegin(GL_QUADS)
        for side, face in enumerate(self.CUBE_QUAD_VERTS):
            color = self.CUBE_COLORS[3]
            glColor3fv(color)
            for vert in face:
                pos = self.CUBE_POINTS[vert]
                glVertex3fv(pos)
        glEnd()

        for side, led_matrix in enumerate(self.led_states):
            scale = 1 / self.LED_MATRIX_SIZE
            
            if side == 0:
                self.draw_led_matrix(led_matrix, pos, scale)
            elif side == 1:
                glPushMatrix()
                glRotatef(-90, 1, 0, 0)
                self.draw_led_matrix(led_matrix, pos, scale)
                glPopMatrix()
            elif side == 2:
                glPushMatrix()
                glRotatef(-90, 0, 1, 0)
                self.draw_led_matrix(led_matrix, pos, scale)
                glPopMatrix()
            elif side == 3:
                glPushMatrix()
                glRotatef(90, 0, 1, 0)
                self.draw_led_matrix(led_matrix, pos, scale)
                glPopMatrix()

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for line in self.CUBE_EDGES:
            for vert in line:
                pos = self.CUBE_POINTS[vert]
                glVertex3fv(pos)
        glEnd()

    def main(self):
        
        print("test")

        print("test")
        self.display = (800, 600)
        pygame.init()
        pygame.display.set_mode(self.display, OPENGL | DOUBLEBUF)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, self.display[0] / self.display[1], 0.1, 100.0)
        glTranslatef(0.0, 0.0, -3.0)
        glRotatef(25, 1, 0, 0)

        self.rotate_angle_x = 0  # Initialer Drehwinkel
        self.rotate_angle_y = 0
        self.speed = 4
        self.clock = pygame.time.Clock()
        

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.rotate_angle_x += self.speed
                    elif event.key == pygame.K_d:
                        self.rotate_angle_x -= self.speed
                    if event.key == pygame.K_w:
                        self.rotate_angle_y += self.speed
                    elif event.key == pygame.K_s:
                        self.rotate_angle_y -= self.speed
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        self.rotate_angle_x = 0
                    if event.key in [pygame.K_w, pygame.K_s]:
                        self.rotate_angle_y = 0

            glClearColor(0.8, 0.8, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glRotatef(self.rotate_angle_x, 0, 1, 0)
            glRotatef(self.rotate_angle_y, 1, 0, 0)

            colorSize1 = random.randint(0, self.LED_MATRIX_SIZE * self.LED_MATRIX_SIZE * 2)
            colorSize0 = random.randint(0, self.LED_MATRIX_SIZE * self.LED_MATRIX_SIZE * 2)

            #self.setColor(0, [(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)) if i < colorSize1 else None for i in range(self.LED_MATRIX_SIZE * self.LED_MATRIX_SIZE * 2)])
            #self.setColor(1, [(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)) if i < colorSize0 else None for i in range(self.LED_MATRIX_SIZE * self.LED_MATRIX_SIZE * 2)])
            #self.write()

            self.drawcube()
            pygame.display.flip()
            self.clock.tick(60)

    def setColor(self, index: int, colors: list):
        
        for i, matrixData in enumerate(self.led_states):
            for y, yData in enumerate(matrixData):
                for x, yData in enumerate(yData):
                    Lx = x
                    Ly = self.LED_MATRIX_SIZE - y - 1
                    indexStrip, stripIndex = self.pos_to_pixel(self.sides[i], Lx, Ly)
                    
                    if indexStrip == index:

                        if len(colors) <= stripIndex:
                            self.led_states_buff[i][y][x] = None
                        else:
                            self.led_states_buff[i][y][x] = colors[stripIndex]

    def pos_to_pixel(self, side, x, y):
        SIZE = self.LED_MATRIX_SIZE
        if x >= SIZE or x < 0 or y >= SIZE or y < 0:
            return [-1, 0]

        i = 0  # strip index
        max_val = SIZE * SIZE * 2
        if side == "front":
            if y % 2 == 0:
                i = x + (y * SIZE) + (SIZE * (y + 1))
            else:
                i = (y * SIZE) + (SIZE * (y + 1)) - 1 - x
        elif side == "left":
            if y % 2 == 0:
                i = x + (y * SIZE * 2)
            else:
                i = y * SIZE * 2 + SIZE * 2 - x - 1
        elif side == "top":
            if y % 2 == 0:
                i = max_val - (x + (SIZE * y * 2) + 1)
            else:
                i = max_val - ((SIZE - x - 1) + (y * (SIZE * 2) + SIZE) + 1)
        elif side == "right":
            zero = max_val - SIZE * 2
            if x % 2 == 0:
                i = (zero - x * SIZE * 2) + y
            else:
                i = (zero - (x - 1) * SIZE * 2) - 1 - y
        if side == "left" or side == "front":
            return [0, i]
        if side == "top" or side == "right":
            return [1, i]

    def write(self):
        self.led_states = self.led_states_buff

    def clear(self):
        self.led_states_buff = [[[None for _ in range(self.LED_MATRIX_SIZE)] for _ in range(self.LED_MATRIX_SIZE)] for _ in range(4)]
        self.write()

if __name__ == "__main__":
    demo = Gigacube()
    demo.main()
