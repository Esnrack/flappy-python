from OpenGL.GL import *
from OpenGL.GLUT import *
import config

def draw_clouds():
    for cloud in config.clouds:
        cloud.draw()

def draw_ground(world_x_min=-1.5, world_x_max=1.5, use_fallback_color=False):

    x_min, x_max = world_x_min, world_x_max
    y_min, y_max = -1.0, -0.9

    if use_fallback_color or not config.ground_texture_id:
        glColor3f(0.6, 0.3, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(x_min, y_max)
        glVertex2f(x_max, y_max)
        glVertex2f(x_max, y_min)
        glVertex2f(x_min, y_min)
        glEnd()
        if not use_fallback_color:
            glColor3f(1.0, 1.0, 1.0)
    else:
        quad_width = x_max - x_min
        tile_world_width = config.GROUND_TILE_WORLD_WIDTH
        horizontal_repeats = quad_width / tile_world_width if tile_world_width > 0 else 1.0
        quad_height = y_max - y_min
        tile_world_height = tile_world_width
        vertical_repeats = quad_height / tile_world_height if tile_world_height > 0 else 1.0
        U0_offset = config.ground_offset_x
        U_REPEAT_offset = config.ground_offset_x + horizontal_repeats
        V0_base = 0.0
        V_REPEAT = vertical_repeats

        glBegin(GL_QUADS)
        glTexCoord2f(U0_offset, V0_base)
        glVertex2f(x_min, y_max)
        glTexCoord2f(U_REPEAT_offset, V0_base)
        glVertex2f(x_max, y_max)
        glTexCoord2f(U_REPEAT_offset, V_REPEAT)
        glVertex2f(x_max, y_min)
        glTexCoord2f(U0_offset, V_REPEAT)
        glVertex2f(x_min, y_min)
        glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))