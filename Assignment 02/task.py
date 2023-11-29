from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import os

WIDTH, HEIGHT = 600, 800
BACKGROUND_COLOR = 0.0, 0.0, 0.0, 1.0

red_rgb = 1.0, 0.0, 0.0
green_rgb = 0.0, 1.0, 0.0
blue_rgb = 0.0, 0.0, 1.0
yellow_rgb = 1.0, 1.0, 0.0

RUNNING = True
GAME_PLAY = True
POINT = 0


def draw_points(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx >= 0 and dy >= 0:
        if dx >= dy:
            return 0
        else:
            return 1
    elif dx < 0 and dy >= 0:
        if -dx >= dy:
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if dx <= dy:
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
        if dx >= -dy:
            return 7
        else:
            return 6


def toZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def drawLine(x1, y1, x2, y2, size):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = toZoneZero(x1, y1, zone)
    x2, y2 = toZoneZero(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    de = 2 * dy
    dne = 2 * (dy - dx)
    x = x1
    y = y1
    while x <= x2:
        real_x, real_y = toZoneZero(x, y, zone)
        draw_points(real_x, real_y, size)
        if d <= 0:
            d = d + de
            x = x + 1
        else:
            d = d + dne
            x = x + 1
            y = y + 1


def drawLeftArrow(size):
    drawLine(25, 750, 75, 750, size)
    drawLine(25, 750, 50, 775, size)
    drawLine(25, 750, 50, 725, size)


def cross(size):
    drawLine(525, 725, 575, 775, size)
    drawLine(575, 725, 525, 775, size)


def play(size):
    drawLine(280, 725, 280, 775, size)
    drawLine(280, 775, 325, 750, size)
    drawLine(280, 725, 325, 750, size)


def pause(size):
    drawLine(280, 725, 280, 775, size)
    drawLine(320, 725, 320, 775, size)


def drawDimond(x1, y1, x2, y2, x3, y3, x4, y4, size):
    drawLine(x1, y1, x2, y2, size)
    drawLine(x2, y2, x3, y3, size)
    drawLine(x3, y3, x4, y4, size)
    drawLine(x4, y4, x1, y1, size)


def drawBowl(x1, y1, x2, y2, x3, y3, x4, y4, size):
    drawLine(x1, y1, x2, y2, size)
    drawLine(x2, y2, x3, y3, size)
    drawLine(x3, y3, x4, y4, size)
    drawLine(x4, y4, x1, y1, size)


class Diamond:
    def __init__(self, x, y, w, h, speed, size):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.size = size
        self.speed = speed
        self.color = (random.random(), random.random(), random.random())

    def draw(self):
        x1 = self.x + self.width / 2
        y1 = self.y
        x2 = self.x
        y2 = self.y + self.height / 2
        x3 = self.x + self.width / 2
        y3 = self.y + self.height
        x4 = self.x + self.width
        y4 = self.y + self.height / 2

        drawDimond(x1, y1, x2, y2, x3, y3, x4, y4, self.size)

    def move(self):
        self.y -= self.speed

    def checkCollision(self, catcher):
        if self.y <= 50:
            return False
        if (
            self.x < catcher.x + catcher.width
            and self.x + self.width > catcher.x
            and self.y < catcher.y + catcher.height
            and self.y + self.height > catcher.y
        ):
            return True
        return False

    def checkMiss(self):
        if self.y <= 50:
            return True
        return False

    def update(self):
        self.move()
        glColor3f(*self.color)
        self.draw()


class Catcher:
    def __init__(self, x, y, w, h, speed, size):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.size = size
        self.speed = speed
        self.color = 1.0, 1.0, 1.0

    def draw(self):
        x1 = self.x
        y1 = self.y
        x2 = self.x + (self.width // 3)
        y2 = self.y - self.height
        x3 = self.x + (self.width // 3) * 2
        y3 = self.y - self.height
        x4 = self.x + self.width
        y4 = self.y
        drawBowl(x1, y1, x2, y2, x3, y3, x4, y4, self.size)

    def moveLeft(self):
        if self.x - self.speed >= 0:
            self.x -= self.speed

    def moveRight(self):
        if self.x + self.speed <= WIDTH - self.width:
            self.x += self.speed

    def update(self):
        glColor3f(*self.color)
        self.draw()


# initial Diamond
dimond_x = random.randint(25, WIDTH - 25)
dimond_speed = 1
dimond_speed_limit = 5
DIMOND = Diamond(dimond_x, HEIGHT - 50, 50, 50, dimond_speed, 2)

# initial Catcher
catcher_x = WIDTH // 2
catcher_y = 50
catcher_width = 100
catcher_height = 25
catcher_speed = 2
catcher_speed_limit = 5
CATCHER = Catcher(catcher_x, catcher_y, catcher_width, catcher_height, catcher_speed, 2)


def gamePlay():
    global DIMOND, CATCHER, RUNNING, POINT, dimond_speed
    if DIMOND.checkCollision(CATCHER):
        POINT += 1
        print("Score: ", POINT)
        DIMOND.x = random.randint(50, WIDTH - 50)
        DIMOND.y = HEIGHT - 50
        DIMOND.color = (random.random(), random.random(), random.random())
        if dimond_speed <= dimond_speed_limit:
            DIMOND.speed += 0.5
        if CATCHER.speed <= catcher_speed_limit:
            CATCHER.speed += 0.3

    elif DIMOND.checkMiss():
        print("Game Over")
        print("Score: ", POINT)
        RUNNING = False
        CATCHER.color = red_rgb

    DIMOND.update()


def keyPressed(key, x, y):
    global CATCHER, RUNNING
    if RUNNING and GAME_PLAY:
        if key == b"a":
            if CATCHER.x >= 0:
                CATCHER.moveLeft()
        elif key == b"d":
            if CATCHER.x <= WIDTH - CATCHER.width:
                CATCHER.moveRight()


def mouseClick(button, state, x, y):
    global RUNNING, GAME_PLAY, POINT, dimond_speed, DIMOND, CATCHER
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if x >= 250 and x <= 350 and y >= 0 and y <= 100 and RUNNING:
            GAME_PLAY = not GAME_PLAY
            # print("########################## Mouse Click")
        elif x >= 0 and x <= 100 and y >= 0 and y <= 100:
            reset()
        elif x >= 500 and x <= 600 and y >= 0 and y <= 100:
            RUNNING = False
            GAME_PLAY = False
            print("Goodbye")
            print("Score: ", POINT)
            glutLeaveMainLoop()
            os._exit(0)


def reset():
    global RUNNING, GAME_PLAY, POINT, dimond_speed, DIMOND, CATCHER
    RUNNING = True
    GAME_PLAY = True
    POINT = 0

    # reset Diamond
    DIMOND.x = random.randint(50, WIDTH - 50)
    DIMOND.y = HEIGHT - 50
    DIMOND.color = (random.random(), random.random(), random.random())
    DIMOND.speed = 1
    DIMOND.color = (random.random(), random.random(), random.random())

    # reset Catcher
    CATCHER.x = WIDTH // 2
    CATCHER.y = 50
    CATCHER.width = 100
    CATCHER.height = 25
    CATCHER.speed = 2
    CATCHER.color = 1.0, 1.0, 1.0


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global RUNNING, dimond_speed, DIMOND, CATCHER
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(*green_rgb)
    drawLeftArrow(2)

    if GAME_PLAY:
        glColor3f(*yellow_rgb)
        pause(2)  # pause
    else:
        glColor3f(*blue_rgb)
        play(2)  # play

    glColor3f(*red_rgb)
    cross(2)  # cross

    if RUNNING:
        if GAME_PLAY:
            gamePlay()
        else:
            DIMOND.draw()

    CATCHER.update()

    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Catch the Diamonds!")  # window name
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouseClick)

    glutMainLoop()


if __name__ == "__main__":
    main()
