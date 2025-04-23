# player.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import config # Importa as configurações globais

def draw_bird():
    """Desenha o pássaro na tela usando sua sprite sheet e animação."""

    if config.invulnerable and int(time.time() * 10) % 2 == 0:
        return # Pisca se invulnerável

    if not config.bird_texture_id or not config.bird_frames_uv:
        # Fallback: Desenhar um quadrado amarelo
        glColor3f(1.0, 1.0, 0.0)
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        half_w_fb = (config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W) / 2.0
        half_h_fb = (config.BIRD_DRAW_HEIGHT * config.BIRD_COLLISION_SCALE_H) / 2.0
        glVertex2f(config.BIRD_X - half_w_fb, config.BIRD_Y - half_h_fb)
        glVertex2f(config.BIRD_X + half_w_fb, config.BIRD_Y - half_h_fb)
        glVertex2f(config.BIRD_X + half_w_fb, config.BIRD_Y + half_h_fb)
        glVertex2f(config.BIRD_X - half_w_fb, config.BIRD_Y + half_h_fb)
        glEnd()
        return

    # --- Desenho com Textura ---
    current_frame_index = config.bird_current_frame % len(config.bird_frames_uv)
    try:
        u0, v0, u1, v1 = config.bird_frames_uv[current_frame_index] # u0=left, u1=right; v0=bottom, v1=top
    except IndexError: return # Segurança

    glBindTexture(GL_TEXTURE_2D, config.bird_texture_id)

    # Calcula tamanho de DESENHO, aplicando shrink se ativo
    current_size_scale = config.SHRINK_SCALE_FACTOR if config.shrink_active else 1.0
    draw_w = config.BIRD_DRAW_WIDTH * current_size_scale
    draw_h = (draw_w / config.bird_frame_aspect) if config.bird_frame_aspect > 0 else draw_w
    half_w = draw_w / 2.0
    half_h = draw_h / 2.0

    x0, y0 = config.BIRD_X - half_w, config.BIRD_Y - half_h # Inferior esquerdo Vértice
    x1, y1 = config.BIRD_X + half_w, config.BIRD_Y + half_h # Superior direito Vértice

    # Desenha o Quad mapeando os cantos da textura
    # !! CORREÇÃO AQUI: Inverter u0 e u1 para flip horizontal !!
    glBegin(GL_QUADS)
    # Vértice Inferior Esquerdo (x0, y0) usa UV Superior DIREITO (u1, v1)
    glTexCoord2f(u1, v1)
    glVertex2f(x0, y0)
    # Vértice Inferior Direito (x1, y0) usa UV Superior ESQUERDO (u0, v1)
    glTexCoord2f(u0, v1)
    glVertex2f(x1, y0)
    # Vértice Superior Direito (x1, y1) usa UV Inferior ESQUERDO (u0, v0)
    glTexCoord2f(u0, v0)
    glVertex2f(x1, y1)
    # Vértice Superior Esquerdo (x0, y1) usa UV Inferior DIREITO (u1, v0)
    glTexCoord2f(u1, v0)
    glVertex2f(x0, y1)
    glEnd()