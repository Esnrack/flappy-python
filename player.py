# player.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import config # Importa as configurações globais

def draw_bird():
    """Desenha o pássaro na tela usando sua sprite sheet e animação."""

    # Lógica para piscar quando invulnerável
    # Pisca a cada 0.1 segundos (10 vezes por segundo)
    if config.invulnerable and int(time.time() * 10) % 2 == 0:
        return # Não desenha neste frame para criar o efeito de piscar

    # Verifica se a textura e os frames estão carregados
    if not config.bird_texture_id or not config.bird_frames_uv:
        # Fallback: Desenhar um quadrado amarelo
        # print("Aviso: Textura/UVs do pássaro não carregados, desenhando fallback.")
        glColor3f(1.0, 1.0, 0.0) # Amarelo
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        half_size = config.BIRD_COLLISION_RADIUS # Usa raio de colisão para fallback
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y + half_size)
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y + half_size)
        glEnd()
        # glIsEnabled(GL_TEXTURE_2D) para verificar se precisa reabilitar,
        # mas main.py/render() gerencia isso globalmente.
        return

    # --- Desenho com Textura ---
    # Garante que o frame atual é válido
    current_frame_index = config.bird_current_frame % len(config.bird_frames_uv)
    try:
        u0, v0, u1, v1 = config.bird_frames_uv[current_frame_index]
    except IndexError:
         # Caso MUITO raro se len(config.bird_frames_uv) for 0 após a verificação inicial
         print(f"Erro crítico: Lista de frames UV do pássaro vazia ou índice inválido ({current_frame_index}).")
         return # Não pode desenhar

    # Ativa (bind) a textura do pássaro
    glBindTexture(GL_TEXTURE_2D, config.bird_texture_id)

    # Calcula as coordenadas dos vértices do Quad
    half_w = config.BIRD_DRAW_WIDTH / 2.0
    half_h = config.BIRD_DRAW_HEIGHT / 2.0
    x0, y0 = config.BIRD_X - half_w, config.BIRD_Y - half_h # Inferior esquerdo
    x1, y1 = config.BIRD_X + half_w, config.BIRD_Y + half_h # Superior direito

    # Desenha o Quad mapeando os cantos da textura
    # glColor já foi definido em render()
    glBegin(GL_QUADS)
    glTexCoord2f(u0, v0); glVertex2f(x0, y0) # Inferior esquerdo
    glTexCoord2f(u1, v0); glVertex2f(x1, y0) # Inferior direito
    glTexCoord2f(u1, v1); glVertex2f(x1, y1) # Superior direito
    glTexCoord2f(u0, v1); glVertex2f(x0, y1) # Superior esquerdo
    glEnd()

    # Não precisa desvincular aqui, render() e draw_powerups() farão bind se necessário