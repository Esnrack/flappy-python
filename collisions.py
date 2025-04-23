# collisions.py
import config
import time
import pause # <<< IMPORTA pause
from powerup import PowerUp

def handle_collision():
    if config.game_over:
        return
    print("Colisão fatal detectada!")
    config.lives -= 1
    print(f"Vidas restantes: {config.lives}")
    if config.lives <= 0:
        config.game_over = True
        config.bird_velocity = 0
        print("Game Over!")
    else:
        config.bird_velocity = 0.0
        config.invulnerable = True
        invulnerability_duration = 2.0
        # --- Usa get_game_time ---
        config.invulnerable_time = pause.get_game_time() + invulnerability_duration
        print(f"Perdeu uma vida! Invulnerável por {invulnerability_duration}s.")

def check_collision():
    """Verifica todas as possíveis colisões do pássaro usando AABB (com shrink)."""
    if not config.game_started or config.game_over:
        return

    # Calcula Hitbox Pássaro
    current_size_scale = config.SHRINK_SCALE_FACTOR if config.shrink_active else 1.0
    bird_collision_w = config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W * current_size_scale
    base_h = (config.BIRD_DRAW_WIDTH / config.bird_frame_aspect) if config.bird_frame_aspect > 0 else config.BIRD_DRAW_WIDTH
    bird_collision_h = base_h * config.BIRD_COLLISION_SCALE_H * current_size_scale
    bird_collision_half_w = bird_collision_w / 2.0
    bird_collision_half_h = bird_collision_h / 2.0
    bird_bottom_edge = config.BIRD_Y - bird_collision_half_h
    bird_top_edge = config.BIRD_Y + bird_collision_half_h
    bird_left_edge = config.BIRD_X - bird_collision_half_w
    bird_right_edge = config.BIRD_X + bird_collision_half_w

    # 1. Colisão Chão/Teto
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

    # 2. Colisão Power-ups
    current_game_time = pause.get_game_time() # Pega tempo de jogo atual
    for powerup in config.powerups:
        if not powerup.collected:
            px, py = powerup.x, powerup.y
            pr = powerup.collision_size
            closest_x = max(bird_left_edge, min(px, bird_right_edge))
            closest_y = max(bird_bottom_edge, min(py, bird_top_edge))
            dist_sq = (px - closest_x)**2 + (py - closest_y)**2
            if dist_sq < (pr * pr):
                print(f"Coletou power-up: {powerup.type}")
                powerup.collected = True
                # --- Aplica Efeitos usando get_game_time ---
                if powerup.type == 'life':
                    config.lives = min(config.lives + 1, config.INITIAL_LIVES)
                    print(f"Ganhou vida! Vidas: {config.lives}")
                elif powerup.type == 'speed':
                    config.speed_multiplier = 2.0
                    config.invulnerable = True
                    boost_duration = 5.0
                    # Usa tempo de jogo para calcular fim
                    config.invulnerable_time = max(config.invulnerable_time, current_game_time + boost_duration)
                    print(f"Speed Boost ativado por {boost_duration}s!")
                elif powerup.type == 'chainsaw':
                    if config.chainsaw_deactivation_pending:
                        config.chainsaw_deactivation_pending = False
                        config.chainsaw_last_pipe_ref = None
                    config.chainsaw_active = True
                    config.chainsaw_pipes_remaining = config.CHAINSAW_DURATION_PIPES
                    print(f"Chainsaw ativado! Gap aumentado por {config.chainsaw_pipes_remaining} canos.")
                elif powerup.type == 'heavy_jump':
                    config.heavy_jump_active = True
                    # Usa tempo de jogo para calcular fim
                    config.heavy_jump_end_time = current_game_time + config.HEAVYJUMP_DURATION_SECONDS
                    print(f"Heavy Jump ativado por {config.HEAVYJUMP_DURATION_SECONDS:.1f} segundos!")
                elif powerup.type == 'shrink':
                    config.shrink_active = True
                     # Usa tempo de jogo para calcular fim
                    config.shrink_end_time = current_game_time + config.SHRINK_DURATION_SECONDS
                    print(f"Shrink ativado por {config.SHRINK_DURATION_SECONDS:.1f} segundos!")
                # --- FIM Efeitos ---

    # 3. Colisão Canos
    if config.invulnerable:
        return
    for pipe in config.pipes:
        pipe_left_edge = pipe['x']
        pipe_right_edge = pipe['x'] + config.PIPE_WIDTH
        horizontal_overlap = bird_right_edge > pipe_left_edge and bird_left_edge < pipe_right_edge
        if horizontal_overlap:
            current_gap = config.PIPE_GAP
            is_chainsaw_effective = config.chainsaw_active or \
                                    (config.chainsaw_deactivation_pending and config.chainsaw_last_pipe_ref == pipe)
            if is_chainsaw_effective:
                current_gap += config.CHAINSAW_GAP_INCREASE
            actual_top_height = pipe['bottom_height'] + current_gap
            hit_bottom_pipe = bird_bottom_edge < pipe['bottom_height']
            hit_top_pipe = bird_top_edge > actual_top_height
            if hit_bottom_pipe or hit_top_pipe:
                handle_collision()
                return