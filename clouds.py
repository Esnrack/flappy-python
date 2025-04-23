# clouds.py
import time
import random
import config # Acessa configurações globais
from OpenGL.GL import * # Necessário para gl* chamadas no método draw

class Cloud:
    """Representa uma nuvem individual no background."""
    def __init__(self, y, sprite_path, speed, scale):
        self.x = 1.5 # Será ajustado em update.py para spawn fora da tela
        self.y = y
        self.sprite_path = sprite_path
        self.speed = speed
        self.scale = scale

        # Estado da Animação
        self.current_frame = 0
        self.last_frame_time = time.time()
        self.animation_direction = 1

        # --- REMOVIDO Aspect Ratio Aleatório ---
        # self.final_aspect_ratio = 1.0 # Default (quadrado)
        # aspect_modifier = random.uniform(1.5, 2.0)
        # if self.sprite_path and self.sprite_path in config.cloud_data:
        #     # ... (código anterior removido) ...
        # else:
        #     self.final_aspect_ratio = aspect_modifier
        # --- FIM REMOÇÃO ---

    # Método para calcular largura de desenho
    def get_draw_dimensions(self):
        """Calcula a largura e altura de desenho baseado na escala e aspect ratio ORIGINAL."""
        base_width = config.CLOUD_BASE_DRAW_WIDTH * self.scale
        aspect = 1.0 # Default para quadrado (fallback)

        # --- USA ASPECT RATIO ORIGINAL ---
        if self.sprite_path and self.sprite_path in config.cloud_data:
            cloud_info = config.cloud_data[self.sprite_path]
            aspect = cloud_info.get('aspect', 1.0)
            if not isinstance(aspect, (int, float)) or aspect <= 0:
                aspect = 1.0
        # --- FIM USO ASPECT ORIGINAL ---

        draw_w = base_width
        draw_h = draw_w / aspect if aspect > 0 else draw_w
        return draw_w, draw_h

    # Método para desenhar
    def draw(self):
        """Desenha esta nuvem específica."""
        has_texture = self.sprite_path and self.sprite_path in config.cloud_data \
                      and 'id' in config.cloud_data[self.sprite_path] \
                      and 'uvs' in config.cloud_data[self.sprite_path]

        draw_w, draw_h = self.get_draw_dimensions() # Pega dimensões com aspect original
        half_w = draw_w / 2.0
        half_h = draw_h / 2.0
        x0, y0 = self.x - half_w, self.y - half_h
        x1, y1 = self.x + half_w, self.y + half_h

        if not has_texture:
            # Fallback: Desenha Quadrado/Retângulo Branco
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
            # Desenha com Textura
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
            glVertex2f(x0, y0) # V-Flip
            glTexCoord2f(u1, v1)
            glVertex2f(x1, y0)
            glTexCoord2f(u1, v0)
            glVertex2f(x1, y1)
            glTexCoord2f(u0, v0)
            glVertex2f(x0, y1)
            glEnd()