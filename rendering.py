from OpenGL.GL import *
from OpenGL.GLUT import *
import config
import time

def draw_ground():
    glColor3f(0.6, 0.3, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.9)
    glVertex2f(1.0, -0.9)
    glVertex2f(1.0, -1.0)
    glVertex2f(-1.0, -1.0)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
