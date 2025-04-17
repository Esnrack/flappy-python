# collisions.py
import config
import time
from powerup import PowerUp # Para type hinting / isinstance se necessário

def handle_collision():
    """Chamado quando uma colisão fatal (chão, teto, cano) ocorre e o jogador não está invulnerável."""
    if config.game_over:
        return

    print("Colisão fatal detectada!")
    config.lives -= 1
    print(f"Vidas restantes: {config.lives}")

    if config.lives <= 0:
        config.game_over = True
        config.bird_velocity = 0 # Para o pássaro ao morrer
        print("Game Over!")
    else:
        # Perdeu uma vida, mas o jogo continua: SEM reset de posição, apenas invulnerabilidade
        config.bird_velocity = 0.0 # Para a velocidade para evitar queda imediata pós-hit
        config.invulnerable = True
        invulnerability_duration = 2.0
        config.invulnerable_time = time.time() + invulnerability_duration
        print(f"Perdeu uma vida! Invulnerável por {invulnerability_duration}s.")


def check_collision():
    """Verifica todas as possíveis colisões do pássaro usando uma hitbox AABB."""
    if not config.game_started or config.game_over:
        return

    # --- Calcula as dimensões e bordas da Hitbox AABB do Pássaro ---
    bird_collision_w = config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W
    bird_collision_h = config.BIRD_DRAW_HEIGHT * config.BIRD_COLLISION_SCALE_H
    bird_collision_half_w = bird_collision_w / 2.0
    bird_collision_half_h = bird_collision_h / 2.0

    bird_bottom_edge = config.BIRD_Y - bird_collision_half_h
    bird_top_edge = config.BIRD_Y + bird_collision_half_h
    bird_left_edge = config.BIRD_X - bird_collision_half_w
    bird_right_edge = config.BIRD_X + bird_collision_half_w
    # --- Fim Cálculo Hitbox Pássaro ---

    # 1. Colisão com Chão e Teto (usando bordas AABB)
    if bird_bottom_edge <= -0.9:
        if not config.invulnerable:
            handle_collision()
        if not config.game_over:
            config.BIRD_Y = -0.9 + bird_collision_half_h
            config.bird_velocity = 0
        return

    if bird_top_edge >= 1.0:
        if not config.invulnerable:
            handle_collision()
        if not config.game_over:
            config.BIRD_Y = 1.0 - bird_collision_half_h
            config.bird_velocity = min(0, config.bird_velocity)
        return

    # 2. Colisão com Power-ups (Círculo vs AABB)
    for powerup in config.powerups:
        if not powerup.collected:
            px, py = powerup.x, powerup.y
            pr = powerup.collision_size # Raio do powerup

            # Encontra o ponto mais próximo na AABB do pássaro ao centro do powerup
            closest_x = max(bird_left_edge, min(px, bird_right_edge))
            closest_y = max(bird_bottom_edge, min(py, bird_top_edge))

            # Calcula a distância quadrada do centro do powerup a este ponto mais próximo
            # Não precisa de math.sqrt pois comparamos distâncias quadradas
            dist_sq = (px - closest_x)**2 + (py - closest_y)**2

            # Verifica se a distância quadrada é menor que o raio do powerup ao quadrado
            if dist_sq < (pr * pr):
                print(f"Coletou power-up: {powerup.type}")
                powerup.collected = True

                # Aplica efeito
                if powerup.type == 'life':
                    config.lives = min(config.lives + 1, config.INITIAL_LIVES * 2)
                    print(f"Ganhou vida! Vidas: {config.lives}")
                elif powerup.type == 'speed':
                    config.speed_multiplier = 2.0
                    config.invulnerable = True
                    boost_duration = 5.0
                    config.invulnerable_time = max(config.invulnerable_time, time.time() + boost_duration)
                    print(f"Speed Boost ativado por {boost_duration}s!")


    # 3. Colisão com Canos (usando AABB do pássaro)
    if config.invulnerable:
        return

    for pipe in config.pipes:
        pipe_left_edge = pipe['x']
        pipe_right_edge = pipe['x'] + config.PIPE_WIDTH

        # Verifica sobreposição Horizontal (AABB vs AABB)
        horizontal_overlap = bird_right_edge > pipe_left_edge and bird_left_edge < pipe_right_edge

        if horizontal_overlap:
            # Verifica colisão Vertical (AABB vs Abertura do Cano)
            hit_bottom_pipe = bird_bottom_edge < pipe['bottom_height']
            hit_top_pipe = bird_top_edge > pipe['top_height']

            if hit_bottom_pipe or hit_top_pipe:
                handle_collision()
                return