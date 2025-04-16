# powerup.py
from OpenGL.GL import *
import config # Acessa configurações globais (texture id, uvs, draw size)
import random # Usado em game_pipes.py para criar powerups

class PowerUp:
    """Representa um item de power-up no jogo."""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # String, ex: 'life' ou 'speed'
        self.collected = False

        # Usa tamanhos definidos em config.py
        self.draw_size = config.POWERUP_DRAW_SIZE       # Tamanho visual
        self.collision_size = config.POWERUP_COLLISION_SIZE # Raio/metade do tamanho para colisão


def draw_powerups():
    """Desenha todos os power-ups ativos usando a sprite sheet."""

    # Verifica se a textura dos power-ups e os UVs foram carregados
    if not config.powerup_texture_id or not config.powerup_uvs:
        # Poderia ter um fallback aqui (desenhar quadrados coloridos), mas vamos omitir por enquanto
        # print("Aviso: Textura/UVs dos power-ups não carregados.")
        return

    # Ativa (bind) a textura dos power-ups (uma vez para todos os powerups neste frame)
    glBindTexture(GL_TEXTURE_2D, config.powerup_texture_id)
    # glColor4f(1.0, 1.0, 1.0, 1.0) # Cor definida globalmente em render()

    # Usa glBegin/glEnd uma vez para desenhar todos os quads (ligeiramente mais eficiente)
    glBegin(GL_QUADS)

    for powerup in config.powerups:
        if not powerup.collected:
            # Pega as coordenadas UV (u0, v0, u1, v1) para este TIPO de power-up
            if powerup.type in config.powerup_uvs:
                u0, v0, u1, v1 = config.powerup_uvs[powerup.type]

                # Calcula as coordenadas dos vértices do Quad na tela
                half_size = powerup.draw_size / 2.0
                x0, y0 = powerup.x - half_size, powerup.y - half_size # Canto inferior esquerdo
                x1, y1 = powerup.x + half_size, powerup.y + half_size # Canto superior direito

                # Adiciona os vértices e coordenadas de textura ao batch
                glTexCoord2f(u0, v0); glVertex2f(x0, y0)
                glTexCoord2f(u1, v0); glVertex2f(x1, y0)
                glTexCoord2f(u1, v1); glVertex2f(x1, y1)
                glTexCoord2f(u0, v1); glVertex2f(x0, y1)
            else:
                # Aviso se um power-up de tipo desconhecido (sem UV mapeado) for encontrado
                print(f"Aviso: Tentando desenhar power-up de tipo não mapeado: {powerup.type}")
                # Poderia desenhar um fallback aqui (ex: quadrado roxo)

    glEnd() # Envia o batch de quads para a GPU

    # Desvincular textura é opcional aqui
    # glBindTexture(GL_TEXTURE_2D, 0)

# Nota: A criação de instâncias de PowerUp acontece em game_pipes.py
# Exemplo de como seria criado lá:
# if random.random() < 0.1: # Chance de criar powerup
#     powerup_type = random.choice(config.POWERUP_TYPES) # Escolhe um tipo válido
#     # A posição Y pode ser aleatória ou relacionada à abertura do cano
#     powerup_y = random.uniform(pipe['bottom_height'] + 0.1, pipe['top_height'] - 0.1)
#     # Cria na mesma posição X inicial do cano
#     config.powerups.append(PowerUp(pipe['x'] + config.PIPE_WIDTH / 2, powerup_y, powerup_type))