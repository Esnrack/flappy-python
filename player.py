# player.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import config # Importa as configurações globais

def draw_bird():
    """Desenha o pássaro na tela usando sua sprite sheet e animação."""

    # Lógica para piscar quando invulnerável
    if config.invulnerable and int(time.time() * 10) % 2 == 0:
        return # Não desenha neste frame para criar o efeito de piscar

    # Verifica se a textura e os frames estão carregados
    if not config.bird_texture_id or not config.bird_frames_uv:
        # Fallback: Desenhar um quadrado amarelo
        glColor3f(1.0, 1.0, 0.0) # Amarelo
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        half_size = config.BIRD_COLLISION_RADIUS
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y + half_size)
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y + half_size)
        glEnd()
        return

    # --- Desenho com Textura ---
    # Garante que o frame atual é válido
    current_frame_index = config.bird_current_frame % len(config.bird_frames_uv)
    try:
        # UVs calculados em main.py: v0=bottom V, v1=top V
        u0, v0, u1, v1 = config.bird_frames_uv[current_frame_index]
    except IndexError:
         print(f"Erro crítico: Lista de frames UV do pássaro vazia ou índice inválido ({current_frame_index}).")
         return

    # Ativa (bind) a textura do pássaro
    glBindTexture(GL_TEXTURE_2D, config.bird_texture_id)

    # Calcula as coordenadas dos vértices do Quad
    half_w = config.BIRD_DRAW_WIDTH / 2.0
    half_h = config.BIRD_DRAW_HEIGHT / 2.0
    x0, y0 = config.BIRD_X - half_w, config.BIRD_Y - half_h # Inferior esquerdo
    x1, y1 = config.BIRD_X + half_w, config.BIRD_Y + half_h # Superior direito

    # Desenha o Quad mapeando os cantos da textura
    # !! CORREÇÃO AQUI: Inverter v0 e v1 na aplicação !!
    glBegin(GL_QUADS)
    # Vértice Inferior Esquerdo (y0) usa Coordenada V Superior da Textura (v1)
    glTexCoord2f(u0, v1); glVertex2f(x0, y0)
    # Vértice Inferior Direito (y0) usa Coordenada V Superior da Textura (v1)
    glTexCoord2f(u1, v1); glVertex2f(x1, y0)
    # Vértice Superior Direito (y1) usa Coordenada V Inferior da Textura (v0)
    glTexCoord2f(u1, v0); glVertex2f(x1, y1)
    # Vértice Superior Esquerdo (y1) usa Coordenada V Inferior da Textura (v0)
    glTexCoord2f(u0, v0); glVertex2f(x0, y1)
    glEnd()