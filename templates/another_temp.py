from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as r

HEIGHT, WIDTH = 500, 500
BACKGROUND_COLOR = (0.0, 0.0, 0.0, 0.0)


def draw_points(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_line(x1, y1, x2, y2, size):
    glLineWidth(size)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_triangle(x1, y1, x2, y2, x3, y3, size):
    glLineWidth(size)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()


# def keyPressed(key, x, y):
#     global DAY
#     if key == b"d" or key == b"D":
#         DAY = True
#     elif key == b"n" or key == b"N":
#         DAY = False
#     print(DAY)


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global BACKGROUND_COLOR
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Task 01")  # window name

    glutDisplayFunc(showScreen)

    # glutKeyboardFunc(keyPressed)

    glutIdleFunc(showScreen)

    glutMainLoop()


if __name__ == "__main__":
    main()
