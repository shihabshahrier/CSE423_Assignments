from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


import random as r

HEIGHT, WIDTH = 800, 800
BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)
CIRCLEs = []
Rate = 1.2
R = 2
PLAY = True


def draw_points(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawCircle(xc, yc, x, y, pix):
    draw_points(xc + x, yc + y, pix)
    draw_points(xc - x, yc + y, pix)
    draw_points(xc + x, yc - y, pix)
    draw_points(xc - x, yc - y, pix)
    draw_points(xc + y, yc + x, pix)
    draw_points(xc - y, yc + x, pix)
    draw_points(xc + y, yc - x, pix)
    draw_points(xc - y, yc - x, pix)


def midPointCircle(xc, yc, r, pix):
    x = 0
    y = r
    drawCircle(xc, yc, x, y, pix)
    d = 1 - r
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * (x - y) + 5
            x += 1
            y -= 1
        drawCircle(xc, yc, x, y, pix)


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        midPointCircle(self.x, self.y, self.r, 2)

    def isNotInside(self):
        return (
            self.x + self.r > WIDTH
            or self.x - self.r < 0
            or self.y + self.r > HEIGHT
            or self.y - self.r < 0
        )

    def update(self):
        self.r += Rate
        self.draw()


def mouseClick(button, state, x, y):
    global CIRCLEs
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if x > 50 and x < WIDTH - 50 and y > 50 and y < HEIGHT - 50:
            circle = Circle(x, HEIGHT - y, R)
            CIRCLEs.append(circle)


def keyPressed(key, x, y):
    global PLAY, Rate
    if key == b" ":
        PLAY = not PLAY
    elif key == GLUT_KEY_RIGHT:
        Rate += 0.2
    elif key == GLUT_KEY_LEFT:
        Rate -= 0.2


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def circleAnimation():
    for i, circle in enumerate(CIRCLEs):
        color = (r.random(), r.random(), r.random())
        glColor3f(*color)
        if circle.isNotInside():
            CIRCLEs.pop(i)
            continue
        if not PLAY:
            circle.draw()
        else:
            circle.update()


def showScreen():
    global BACKGROUND_COLOR
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    circleAnimation()

    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("Task 01")  # window name

    glutDisplayFunc(showScreen)

    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(keyPressed)

    glutMouseFunc(mouseClick)

    glutIdleFunc(showScreen)

    glutMainLoop()


if __name__ == "__main__":
    main()
