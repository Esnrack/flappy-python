# powerup.py.
from OpenGL.GL import *
import config # Acessa configurações globais (texture id, uvs, draw size)
import random # Usado em game_pipes.py
import time

class PowerUp:
    """Representa um item de power-up no jogo."""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # String, ex: 'life' ou 'speed'
        self.collected = False

        # Usa tamanhos definidos em config.py
        self.draw_size = config.POWERUP_DRAW_SIZE       # Tamanho visual
        self.collision_size = config.POWERUP_COLLISION_SIZE # Raio/metade para colisão


def draw_powerups():
    """Desenha todos os power-ups ativos usando a sprite sheet."""

    # Verifica se a textura e UVs estão carregados
    if not config.powerup_texture_id or not config.powerup_uvs:
        # print("Aviso: Textura/UVs dos power-ups não carregados.")
        return

    # Ativa a textura dos power-ups
    glBindTexture(GL_TEXTURE_2D, config.powerup_texture_id)
    # glColor já definido em render()

    glBegin(GL_QUADS) # Batch draw para eficiência

    for powerup in config.powerups:
        # Não desenha se já foi coletado (será removido em update_pipes)
        if not powerup.collected:
            # Pega as coordenadas UV para este TIPO de power-up
            if powerup.type in config.powerup_uvs:
                u0, v0, u1, v1 = config.powerup_uvs[powerup.type]

                # Calcula coordenadas dos vértices
                half_size = powerup.draw_size / 2.0
                x0 = powerup.x - half_size
                y0 = powerup.y - half_size
                x1 = powerup.x + half_size
                y1 = powerup.y + half_size

                # Adiciona vértices e coordenadas de textura ao batch
                glTexCoord2f(u0, v0); glVertex2f(x0, y0)
                glTexCoord2f(u1, v0); glVertex2f(x1, y0)
                glTexCoord2f(u1, v1); glVertex2f(x1, y1)
                glTexCoord2f(u0, v1); glVertex2f(x0, y1)
            else:
                # Aviso se o tipo não tem UV mapeado
                print(f"Aviso: Tentando desenhar power-up de tipo não mapeado: {powerup.type}")

    glEnd() # Envia o batch

    # Não precisa desvincular textura aqui