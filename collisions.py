# collisions.py
import config
import time
from powerup import PowerUp # Importar para type hinting se necessário

def handle_collision():
    """Chamado quando uma colisão fatal (chão, teto, cano) ocorre."""
    print("Colisão detectada!")
    config.lives -= 1
    print(f"Vidas restantes: {config.lives}")
    if config.lives <= 0:
        config.game_over = True
        print("Game Over!")
    else:
        # Resetar posição e velocidade, dar invulnerabilidade temporária
        config.BIRD_Y = 0.0
        config.bird_velocity = 0.0
        config.invulnerable = True
        config.invulnerable_time = time.time() + 2.0 # 2 segundos de invulnerabilidade
        print("Perdeu uma vida! Invulnerável por 2s.")


def check_collision():
    """Verifica todas as possíveis colisões do pássaro."""

    # 1. Colisão com Chão e Teto (usando raio de colisão)
    bird_bottom_edge = config.BIRD_Y - config.BIRD_COLLISION_RADIUS
    bird_top_edge = config.BIRD_Y + config.BIRD_COLLISION_RADIUS

    # Colisão com o chão (-0.9 é a coordenada Y do topo do chão)
    if bird_bottom_edge < -0.9:
        print("Colisão com o chão.")
        if not config.invulnerable:
            handle_collision()
        # Mesmo invulnerável, impede de cair mais (pode ajustar se quiser que atravesse)
        config.BIRD_Y = -0.9 + config.BIRD_COLLISION_RADIUS
        config.bird_velocity = 0 # Para não quicar
        return # Se colidiu com chão/teto, não verifica mais nada neste frame

    # Colisão com o teto (1.0 é a coordenada Y do topo da tela visível)
    if bird_top_edge > 1.0:
        print("Colisão com o teto.")
        if not config.invulnerable:
            handle_collision()
        # Impede de subir mais
        config.BIRD_Y = 1.0 - config.BIRD_COLLISION_RADIUS
        config.bird_velocity = 0 # Impede de ficar preso no teto
        return # Se colidiu com chão/teto, não verifica mais nada neste frame


    # 2. Colisão com Power-ups (antes dos canos, para poder coletar e bater quase ao mesmo tempo)
    # Iterar sobre uma cópia da lista permite remover itens durante a iteração
    for powerup in list(config.powerups):
        if not powerup.collected:
            # Colisão Círculo-Círculo (mais precisa para sprites arredondados)
            distance_sq = (config.BIRD_X - powerup.x)**2 + (config.BIRD_Y - powerup.y)**2
            collision_distance_sq = (config.BIRD_COLLISION_RADIUS + powerup.collision_size)**2

            if distance_sq < collision_distance_sq:
                print(f"Coletou power-up: {powerup.type}")
                powerup.collected = True # Marca como coletado (será removido depois)

                # Aplica efeito do power-up
                if powerup.type == 'life':
                    # Limita as vidas a um máximo (ex: dobro das iniciais)
                    config.lives = min(config.lives + 1, config.INITIAL_LIVES * 2)
                    print(f"Ganhou vida! Vidas: {config.lives}")
                elif powerup.type == 'speed':
                    config.speed_multiplier = 2.0 # Dobra a velocidade do jogo
                    # Dá invulnerabilidade enquanto o speed boost durar
                    config.invulnerable = True
                    config.invulnerable_time = time.time() + 5.0 # Duração do speed boost (ex: 5s)
                    print(f"Speed Boost ativado por 5s!")

                # Remove o power-up da lista principal após coletar
                # É mais seguro fazer a remoção fora do loop principal de update/render
                # A linha `config.powerups[:] = [p for p in config.powerups if ...]` em `update_pipes` já faz isso.
                # Mas se precisar remover imediatamente:
                # config.powerups.remove(powerup)


    # 3. Colisão com Canos
    if config.invulnerable: # Se está invulnerável, não verifica colisão com canos
         return

    bird_left_edge = config.BIRD_X - config.BIRD_COLLISION_RADIUS
    bird_right_edge = config.BIRD_X + config.BIRD_COLLISION_RADIUS

    for pipe in config.pipes:
        pipe_left_edge = pipe['x']
        pipe_right_edge = pipe['x'] + config.PIPE_WIDTH

        # Verifica se há sobreposição horizontal entre o pássaro e o cano
        horizontal_overlap = bird_right_edge > pipe_left_edge and bird_left_edge < pipe_right_edge

        if horizontal_overlap:
            # Se há sobreposição horizontal, verifica a vertical
            is_above_bottom_pipe = bird_bottom_edge < pipe['bottom_height']
            is_below_top_pipe = bird_top_edge > pipe['top_height']

            if is_above_bottom_pipe or is_below_top_pipe:
                # Colisão vertical detectada!
                print("Colisão com cano!")
                handle_collision()
                return # Para a verificação, só pode colidir com um cano por vez