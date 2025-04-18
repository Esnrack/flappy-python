# powerup.py
from OpenGL.GL import *
import config # Acessa configurações globais (texture id, uvs, draw size)
import random # Usado em game_pipes.py

class PowerUp:
    """Representa um item de power-up no jogo."""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # String, ex: 'life' ou 'speed'
        self.collected = False
        self.draw_size = config.POWERUP_DRAW_SIZE
        self.collision_size = config.POWERUP_COLLISION_SIZE


def draw_powerups():
    """Desenha todos os power-ups ativos usando a sprite sheet."""

    if not config.powerup_texture_id or not config.powerup_uvs:
        return

    glBindTexture(GL_TEXTURE_2D, config.powerup_texture_id)

    glBegin(GL_QUADS) # Batch draw

    for powerup in config.powerups:
        if not powerup.collected:
            if powerup.type in config.powerup_uvs:
                # UVs calculados em main.py: v0=bottom V, v1=top V
                u0, v0, u1, v1 = config.powerup_uvs[powerup.type]

                # Calcula coordenadas dos vértices
                half_size = powerup.draw_size / 2.0
                x0, y0 = powerup.x - half_size, powerup.y - half_size # Bottom-left
                x1, y1 = powerup.x + half_size, powerup.y + half_size # Top-right

                # Adiciona vértices e coordenadas de textura ao batch
                # !! CORREÇÃO AQUI: Inverter v0 e v1 na aplicação !!
                # Vértice Inferior Esquerdo (y0) usa Coordenada V Superior da Textura (v1)
                glTexCoord2f(u0, v1); glVertex2f(x0, y0)
                # Vértice Inferior Direito (y0) usa Coordenada V Superior da Textura (v1)
                glTexCoord2f(u1, v1); glVertex2f(x1, y0)
                # Vértice Superior Direito (y1) usa Coordenada V Inferior da Textura (v0)
                glTexCoord2f(u1, v0); glVertex2f(x1, y1)
                # Vértice Superior Esquerdo (y1) usa Coordenada V Inferior da Textura (v0)
                glTexCoord2f(u0, v0); glVertex2f(x0, y1)
            else:
                print(f"Aviso: Tentando desenhar power-up de tipo não mapeado: {powerup.type}")

    glEnd() # Envia o batch