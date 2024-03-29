"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unopimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""

import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit

import random

LED_MATRIX_SIZE = 15

# 0 front
# 1 top
# 2 left
# 3 right
led_states = [[[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(LED_MATRIX_SIZE)] for _ in range(LED_MATRIX_SIZE)] for _ in range(4)]
sides = ["front", "top", "left", "right"]


#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge

led_states_buff = [[[(0, 0, 255) for _ in range(LED_MATRIX_SIZE)] for _ in range(LED_MATRIX_SIZE)] for _ in range(4)]


CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
)

CUBE_QUAD_VERTS = (
    (3, 2, 7, 6), (6, 7, 5, 4), (1, 5, 7, 2), (4, 0, 3, 6), (4, 5, 1, 0)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

def setColor(index: int, colors: list):
    global led_states_buff

    for i, matrixData in enumerate(led_states_buff):

        for y, yData in enumerate(matrixData):
            for x, yData in enumerate(yData):
                
                Lx =  x
                Ly = LED_MATRIX_SIZE - y - 1

                indexStrip, stripIndex = pos_to_pixel(sides[i], Lx, Ly)
                
                if indexStrip == index:
                    led_states_buff[i][y][x] = colors[stripIndex]


def pos_to_pixel(side, x, y):

    SIZE = LED_MATRIX_SIZE

    if x >= SIZE or x < 0 or y >= SIZE or y < 0:
        return [-1,0]

    i = 0  # strip index
    max_val = SIZE * SIZE * 2

    # --- first Strip
    if side == "front":
        if y % 2 == 0:  # ->
            i = x + (y * SIZE) + (SIZE * (y + 1))
        else:  # <-
            i = (y * SIZE) + (SIZE * (y + 1)) - 1 - x
    elif side == "left":
        if y % 2 == 0:  # ->
            i = x + (y * SIZE * 2)
        else:  # <-
            i = y * SIZE * 2 + SIZE * 2 - x - 1

    # --- second Strip
    elif side == "top":
        if y % 2 == 0:  # <-
            i = max_val - (x + (SIZE * y * 2) + 1)
        else:  # ->
            i = max_val - ((SIZE - x - 1) + (y * (SIZE * 2) + SIZE) + 1)

    elif side == "right":

        zero = max_val - SIZE * 2

        if x % 2 == 0:  # 1
                        # |
            i = (zero - x * SIZE * 2) + y

        else:  # |
                # y
            i = (zero - (x - 1) * SIZE * 2) - 1 - y  # -1 to get offest

    if side == "left" or side == "front":
        return [0, i]
    if side == "top" or side == "right":
        return [1, i]

    
    


def write():
    global led_states
    led_states = led_states_buff

def clear():
    global led_states_buff
    led_states_buff = [[[None for _ in range(LED_MATRIX_SIZE)] for _ in range(LED_MATRIX_SIZE)] for _ in range(4)]
    write()

setColor(1, [(0, 255, 0) if i < LED_MATRIX_SIZE * 2.5 else None for i in range(LED_MATRIX_SIZE * LED_MATRIX_SIZE * 2)])
write()

def draw_led_matrix(led_matrix, pos, scale):
    offset = 1 / LED_MATRIX_SIZE / 2
    glBegin(GL_QUADS)
    for x in range(LED_MATRIX_SIZE):
        for y in range(LED_MATRIX_SIZE):
            for index, vert in enumerate((6, 7, 5, 4)):
                
                pos = CUBE_POINTS[vert]
                # Definiere die Eckpunkte des Rechtecks, basierend auf den Positionen der Punkte des Würfels
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
                    glColor3f(led_matrix[y][x][0]/255, led_matrix[y][x][1]/255, led_matrix[y][x][2]/255)  # Weiß für beleuchtete LEDs
                    glVertex3f(x_pos, y_pos, pos[2] + 0.01)

                #glVertex3f(x_pos, y_pos, pos[2] + 0.01)  # Skaliere die Positionen, um ein kleineres Rechteck zu erhalten
    glEnd()


def drawcube():
    "draw the cube"
    glBegin(GL_QUADS)
    for side, face in enumerate(CUBE_QUAD_VERTS):
        color = CUBE_COLORS[3]  # Verwende die Farbe des ersten Punktes jeder Seite
        glColor3fv(color)
        for vert in face:
            pos = CUBE_POINTS[vert]
            glVertex3fv(pos)
    glEnd()

    for side, led_matrix in enumerate(led_states):
        scale = 1 / LED_MATRIX_SIZE
        
        if side == 0:  # Für die Vorder- und Rückseite des Würfels
            draw_led_matrix(led_matrix, pos, scale)

        elif side == 1:  # Für die obere Seite des Würfels
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)  # Rotiere die Matrix um -90 Grad um die x-Achse
            draw_led_matrix(led_matrix, pos, scale)
            glPopMatrix()
        elif side == 2:  # Für die linke Seite des Würfels
            glPushMatrix()
            glRotatef(-90, 0, 1, 0)  # Rotiere die Matrix um -90 Grad um die y-Achse
            draw_led_matrix(led_matrix, pos, scale)
            glPopMatrix()
        elif side == 3:  # Für die rechte Seite des Würfels
            glPushMatrix()
            glRotatef(90, 0, 1, 0)  # Rotiere die Matrix um 90 Grad um die y-Achse
            draw_led_matrix(led_matrix, pos, scale)
            glPopMatrix()


    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos = CUBE_POINTS[vert]
            glVertex3fv(pos)
    glEnd()

def main():
    "run the demo"
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, display[0] / display[1], 0.1, 100.0)
    glTranslatef(0.0, 0.0, -3.0)
    glRotatef(25, 1, 0, 0)

    rotate_angle_x = 0  # Initialer Drehwinkel
    rotate_angle_y = 0
    speed = 4

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    rotate_angle_x += speed  # Drehwinkel um 1 Grad erhöhen, wenn "a" gedrückt wird
                elif event.key == pygame.K_d:
                    rotate_angle_x -= speed  # Drehwinkel um 1 Grad verringern, wenn "d" gedrückt wird
                
                if event.key == pygame.K_w:
                    rotate_angle_y += speed  # Drehwinkel um 1 Grad erhöhen, wenn "a" gedrückt wird
                elif event.key == pygame.K_s:
                    rotate_angle_y -= speed  # Drehwinkel um 1 Grad verringern, wenn "d" gedrückt wird
            
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    rotate_angle_x = 0  # Wenn die Taste losgelassen wird, setzen Sie den Drehwinkel auf 0
                if event.key in [pygame.K_w, pygame.K_s]:
                    rotate_angle_y = 0  # Wenn die Taste losgelassen wird, setzen Sie den Drehwinkel auf 0


        glClearColor(0.8, 0.8, 1.0, 1.0)  # Hellblauer Hintergrund
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glRotatef(rotate_angle_x, 0, 1, 0)  # Drehen des Würfels basierend auf dem aktuellen Drehwinkel
        
        glRotatef(rotate_angle_y, 1, 0, 0)
        
        drawcube()
        pygame.display.flip()
        clock.tick(60)

        print(clock.get_fps())


if __name__ == '__main__':
    main()

