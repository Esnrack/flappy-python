# player.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import config # Importa as configurações globais

def draw_bird():
    """Desenha o pássaro na tela usando sua sprite sheet."""

    # Lógica para piscar quando invulnerável
    # Pisca a cada 0.1 segundos (10 vezes por segundo)
    if config.invulnerable and int(time.time() * 10) % 2 == 0:
        return # Não desenha neste frame para criar o efeito de piscar

    # Verifica se a textura do pássaro e os dados dos frames foram carregados
    if not config.bird_texture_id or not config.bird_frames_uv:
        # Fallback: Desenhar um quadrado amarelo simples se a textura falhou
        print("Aviso: Textura do pássaro não carregada, desenhando fallback.")
        glColor3f(1.0, 1.0, 0.0) # Cor amarela
        glDisable(GL_TEXTURE_2D) # Garante que textura está desligada para o fallback
        glBegin(GL_QUADS)
        # Usa o raio de colisão para o tamanho do fallback
        half_size = config.BIRD_COLLISION_RADIUS
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y - half_size)
        glVertex2f(config.BIRD_X + half_size, config.BIRD_Y + half_size)
        glVertex2f(config.BIRD_X - half_size, config.BIRD_Y + half_size)
        glEnd()
        glEnable(GL_TEXTURE_2D) # Reabilita se necessário (embora render() controle)
        return

    # --- Desenho com Textura ---
    # Pega as coordenadas UV (u0, v0, u1, v1) do frame atual da animação
    try:
        u0, v0, u1, v1 = config.bird_frames_uv[config.bird_current_frame]
    except IndexError:
        # Se o índice do frame for inválido, volta para o frame 0 e loga um erro
        print(f"Erro: Índice do frame do pássaro ({config.bird_current_frame}) fora dos limites. Usando frame 0.")
        if not config.bird_frames_uv: # Se a lista está vazia, não há o que fazer
             return
        config.bird_current_frame = 0
        u0, v0, u1, v1 = config.bird_frames_uv[0]


    # Ativa (bind) a textura do pássaro para uso
    glBindTexture(GL_TEXTURE_2D, config.bird_texture_id)

    # Calcula as coordenadas dos vértices do Quad na tela
    # Usa as dimensões de DESENHO definidas em config
    half_w = config.BIRD_DRAW_WIDTH / 2.0
    half_h = config.BIRD_DRAW_HEIGHT / 2.0
    x0, y0 = config.BIRD_X - half_w, config.BIRD_Y - half_h # Canto inferior esquerdo
    x1, y1 = config.BIRD_X + half_w, config.BIRD_Y + half_h # Canto superior direito

    # Desenha o Quad mapeando os cantos da textura para os cantos do Quad
    # glColor4f(1.0, 1.0, 1.0, 1.0) # Cor definida globalmente em render()
    glBegin(GL_QUADS)
    glTexCoord2f(u0, v0) # Coord. textura para canto inferior esquerdo
    glVertex2f(x0, y0)   # Vertice inferior esquerdo

    glTexCoord2f(u1, v0) # Coord. textura para canto inferior direito
    glVertex2f(x1, y0)   # Vertice inferior direito

    glTexCoord2f(u1, v1) # Coord. textura para canto superior direito
    glVertex2f(x1, y1)   # Vertice superior direito

    glTexCoord2f(u0, v1) # Coord. textura para canto superior esquerdo
    glVertex2f(x0, y1)   # Vertice superior esquerdo
    glEnd()

    # Desvincular textura é opcional aqui, pois render() e draw_powerups() farão bind novamente
    # glBindTexture(GL_TEXTURE_2D, 0)