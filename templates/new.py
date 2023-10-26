from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def init():
    glutInit()  # Initialize GLUT
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400, 400)  # Set the window size
    glutCreateWindow("PyOpenGL Example")
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set the clear color (R, G, B, Alpha)
    gluOrtho2D(-1, 1, -1, 1)  # Set the 2D viewing area


def display():
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
    glColor3f(1.0, 1.0, 1.0)  # Set the drawing color (R, G, B)

    glBegin(GL_TRIANGLES)  # Begin drawing triangles
    glVertex2f(0.0, 0.0)
    glVertex2f(0.5, 0.0)
    glVertex2f(0.0, 0.5)
    glEnd()  # End drawing

    glFlush()  # Force the rendering


glutInit(sys.argv)
init()
glutDisplayFunc(display)
glutMainLoop()
