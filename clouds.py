import time
import config
from OpenGL.GL import *
class Cloud:
    def __init__(self, y, sprite_path, speed, scale):
        self.x = 1.5
        self.y = y
        self.sprite_path = sprite_path
        self.speed = speed
        self.scale = scale

        self.current_frame = 0
        self.last_frame_time = time.time()
        self.animation_direction = 1

    def get_draw_dimensions(self):
        base_width = config.CLOUD_BASE_DRAW_WIDTH * self.scale
        aspect = 1.0 

        if self.sprite_path and self.sprite_path in config.cloud_data:
            cloud_info = config.cloud_data[self.sprite_path]
            aspect = cloud_info.get('aspect', 1.0)
            if not isinstance(aspect, (int, float)) or aspect <= 0:
                aspect = 1.0

        draw_w = base_width
        draw_h = draw_w / aspect if aspect > 0 else draw_w
        return draw_w, draw_h

    def draw(self):
        has_texture = self.sprite_path and self.sprite_path in config.cloud_data \
                      and 'id' in config.cloud_data[self.sprite_path] \
                      and 'uvs' in config.cloud_data[self.sprite_path]

        draw_w, draw_h = self.get_draw_dimensions()
        half_w = draw_w / 2.0
        half_h = draw_h / 2.0
        x0, y0 = self.x - half_w, self.y - half_h
        x1, y1 = self.x + half_w, self.y + half_h

        if not has_texture:
            glDisable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 0.8)
            glBegin(GL_QUADS)
            glVertex2f(x0, y0)
            glVertex2f(x1, y0)
            glVertex2f(x1, y1)
            glVertex2f(x0, y1)
            glEnd()
            glColor4f(1.0, 1.0, 1.0, 1.0)
        else:
            glEnable(GL_TEXTURE_2D)
            cloud_info = config.cloud_data[self.sprite_path]
            tex_id = cloud_info['id']
            uvs_list = cloud_info['uvs']
            num_frames = len(uvs_list)

            if num_frames == 0:
                return

            frame_index = self.current_frame % num_frames

            try:
                u0, v0, u1, v1 = uvs_list[frame_index]
            except IndexError:
                return

            glBindTexture(GL_TEXTURE_2D, tex_id)
            glColor4f(1.0, 1.0, 1.0, 1.0)
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