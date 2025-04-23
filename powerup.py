# powerup.py
from OpenGL.GL import *
import config # Acessa configurações globais (texture id, uvs, draw size)
import random # Usado em game_pipes.py
import time # Para animação

class PowerUp:
    """Representa um item de power-up no jogo."""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.collected = False
        # Tamanho de desenho agora é a LARGURA base
        self.draw_width = config.POWERUP_DRAW_SIZE # Largura base
        self.collision_size = config.POWERUP_COLLISION_SIZE
        # Estado da Animação
        self.current_frame = 0 # Inicializa como inteiro
        self.last_frame_time = time.time()
        self.animation_direction = 1


def draw_powerups():
    """Desenha power-ups respeitando o aspect ratio de cada frame."""

    last_bound_texture = -1

    if not config.powerups or not config.powerup_data:
        return

    for powerup in config.powerups:
        if not powerup.collected and powerup.type in config.powerup_data:
            pu_data = config.powerup_data[powerup.type]
            tex_id = pu_data['id']
            uvs_list = pu_data['uvs']
            aspect = pu_data.get('aspect', 1.0) # Pega aspect ratio do frame
            num_frames = len(uvs_list)

            if num_frames == 0:
                continue

            # --- CORREÇÃO: Garante que current_frame é int antes do módulo ---
            frame_index = int(powerup.current_frame) % num_frames
            # --- FIM CORREÇÃO ---

            try:
                u0, v0, u1, v1 = uvs_list[frame_index]
            except IndexError:
                 print(f"Aviso: Índice de frame UV ({frame_index}) inválido para power-up '{powerup.type}'")
                 continue # Pula se o índice for inválido


            glBindTexture(GL_TEXTURE_2D, tex_id)

            # Calcula dimensões de desenho baseadas no aspect ratio
            draw_w = powerup.draw_width
            draw_h = draw_w / aspect if aspect > 0 else draw_w
            half_w = draw_w / 2.0
            half_h = draw_h / 2.0

            # Calcula coordenadas dos vértices
            x0 = powerup.x - half_w
            y0 = powerup.y - half_h
            x1 = powerup.x + half_w
            y1 = powerup.y + half_h

            # Desenha o Quad
            glBegin(GL_QUADS)
            glTexCoord2f(u0, v1); glVertex2f(x0, y0) # V-Flip
            glTexCoord2f(u1, v1); glVertex2f(x1, y0)
            glTexCoord2f(u1, v0); glVertex2f(x1, y1)
            glTexCoord2f(u0, v0); glVertex2f(x0, y1)
            glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)