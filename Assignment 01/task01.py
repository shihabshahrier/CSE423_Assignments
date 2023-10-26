from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as r


WIDTH, HEIGHT = 1280, 720

# BLACK_COLOR = 0.0, 0.0, 0.0, 1.0
# WHITE_COLOR = 1.0, 1.0, 1.0, 1.0
BACKGROUND_COLOR = 1.0, 1.0, 1.0, 1.0


# white_rgb = (1.0, 1.0, 1.0)
# black_rgb = (0.0, 0.0, 0.0)
yellow_rgb = (1.0, 1.0, 0.0)

c_rgb = (0.0, 0.0, 0.0)

DAY = True
key_pressed = None


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


def rain():
    global c_rgb
    if DAY:
        c_rgb = 0.0, 0.0, 0.0
    else:
        c_rgb = 1.0, 1.0, 1.0
    glColor3f(*c_rgb)
    for i in range(1, WIDTH, 20):
        h = HEIGHT
        for j in range(12):
            rand_i = r.randint(10, 20)
            draw_line(i, h, i, h - rand_i, 2)
            h = h - rand_i - 10


def drawHome():
    global DAY
    global c_rgb
    if DAY:
        c_rgb = 0.0, 0.0, 0.0
    else:
        c_rgb = 1.0, 1.0, 1.0
    glColor3f(*c_rgb)
    # draw_triangle(320, 400, 980, 400, 640, 550)
    line_pix = 40
    # roof outline
    draw_line(320, 400, 980, 400, line_pix)
    draw_line(320, 400, 640, 550, line_pix)
    draw_line(640, 550, 980, 400, line_pix)

    # roof inner
    if DAY:
        glColor3f(*yellow_rgb)
    else:
        glColor3f(0.0, 0.0, 0.0)
    draw_triangle(320, 400, 980, 400, 640, 550, 1)

    # house outline
    glColor3f(*c_rgb)
    draw_line(340, 400, 340, 100, line_pix)
    draw_line(320, 100, 980, 100, line_pix)
    draw_line(960, 100, 960, 400, line_pix)

    # door
    draw_line(440, 100, 440, 300, 10)
    draw_line(435, 300, 525, 300, 10)
    draw_line(520, 300, 520, 100, 10)

    # door knob
    draw_points(500, 200, 10)

    # window
    draw_line(700, 300, 700, 200, 10)
    draw_line(695, 200, 805, 200, 10)
    draw_line(800, 200, 800, 300, 10)
    draw_line(805, 300, 695, 300, 10)

    # window lines
    draw_line(750, 300, 750, 200, 10)
    draw_line(700, 250, 800, 250, 10)


def keyPressed(key, x, y):
    global DAY
    if key == b"d" or key == b"D":
        DAY = True
    elif key == b"n" or key == b"N":
        DAY = False
    print(DAY)


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global BACKGROUND_COLOR
    if DAY:
        BACKGROUND_COLOR = 1.0, 1.0, 1.0, 1.0
    else:
        BACKGROUND_COLOR = 0.0, 0.0, 0.0, 1.0
    glClearColor(*BACKGROUND_COLOR)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    rain()
    drawHome()
    glutSwapBuffers()


def main():
    glutInit()

    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)  # window size
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Task 01")  # window name

    glutDisplayFunc(showScreen)

    glutKeyboardFunc(keyPressed)

    glutIdleFunc(showScreen)

    glutMainLoop()


if __name__ == "__main__":
    main()
