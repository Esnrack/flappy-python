# rendering.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import config
import time # Não usado diretamente aqui, mas mantido por histórico

def draw_ground():
    """Desenha o chão como um retângulo marrom na base."""
    glColor3f(0.6, 0.3, 0.1) # Cor marrom
    glBegin(GL_QUADS)
    glVertex2f(-1.5, -0.9) # Estendido um pouco para fora da visão ortográfica padrão
    glVertex2f(1.5, -0.9)
    glVertex2f(1.5, -1.0)
    glVertex2f(-1.5, -1.0)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Desenha texto na tela usando GLUT."""
    # Certifique-se que o blending está ativado se quiser texto sobre elementos
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glDisable(GL_TEXTURE_2D) # Texto não usa textura padrão

    glColor3f(0.0, 0.0, 0.0) # Cor preta para o texto
    # Define a posição do raster (onde o texto começa) nas coordenadas do mundo
    glRasterPos2f(x, y)
    # Desenha cada caractere
    for char in text:
        glutBitmapCharacter(font, ord(char))

    # Reabilita a textura se outros elementos a usarem (gerenciado em render())
    # glEnable(GL_TEXTURE_2D)