
from OpenGL.GL import *
import config
import random
import time

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.collected = False
    
        self.draw_width = config.POWERUP_DRAW_SIZE
        self.collision_size = config.POWERUP_COLLISION_SIZE
    
        self.current_frame = 0
        self.last_frame_time = time.time()
        self.animation_direction = 1


def draw_powerups():
    if not config.powerups or not config.powerup_data:
        return

    for powerup in config.powerups:
        if not powerup.collected and powerup.type in config.powerup_data:
            pu_data = config.powerup_data[powerup.type]
            tex_id = pu_data['id']
            uvs_list = pu_data['uvs']
            aspect = pu_data.get('aspect', 1.0)
            num_frames = len(uvs_list)

            if num_frames == 0:
                continue

            frame_index = int(powerup.current_frame) % num_frames

            try:
                u0, v0, u1, v1 = uvs_list[frame_index]
            except IndexError:
                 print(f"Aviso: Índice de frame UV ({frame_index}) inválido para power-up '{powerup.type}'")
                 continue

            glBindTexture(GL_TEXTURE_2D, tex_id)

            draw_w = powerup.draw_width
            draw_h = draw_w / aspect if aspect > 0 else draw_w
            half_w = draw_w / 2.0
            half_h = draw_h / 2.0

            x0 = powerup.x - half_w
            y0 = powerup.y - half_h
            x1 = powerup.x + half_w
            y1 = powerup.y + half_h

            glBegin(GL_QUADS)
            glTexCoord2f(u0, v1)
            glVertex2f(x0, y0)
            glTexCoord2f(u1, v1)
            glVertex2f(x1, y0)
            glTexCoord2f(u1, v0)
            glVertex2f(x1, y1)
            glTexCoord2f(u0, v0)
            glVertex2f(x0, y1)
            glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)