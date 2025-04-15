from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import numpy as np
import config

def draw_bird():
    if config.invulnerable and int(time.time() * 2) % 2 == 0:
        return

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(config.BIRD_X, config.BIRD_Y)
    for i in range(9):
        angle = i * 2 * np.pi / 8
        glVertex2f(config.BIRD_X + np.cos(angle) * config.BIRD_SIZE,
                   config.BIRD_Y + np.sin(angle) * config.BIRD_SIZE)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(config.BIRD_X + config.BIRD_SIZE * 0.3,
               config.BIRD_Y + config.BIRD_SIZE * 0.2)
    glEnd()
