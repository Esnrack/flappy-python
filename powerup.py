from OpenGL.GL import *
import config

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.size = 0.05
        self.collected = False

def draw_powerups():
    for powerup in config.powerups:
        if not powerup.collected:
            if powerup.type == 'life':
                glColor3f(1.0, 0.0, 0.0)
            else:
                glColor3f(0.0, 0.0, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(powerup.x - powerup.size, powerup.y - powerup.size)
            glVertex2f(powerup.x + powerup.size, powerup.y - powerup.size)
            glVertex2f(powerup.x + powerup.size, powerup.y + powerup.size)
            glVertex2f(powerup.x - powerup.size, powerup.y + powerup.size)
            glEnd()
