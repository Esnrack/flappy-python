# update.py
import config
import time
from game_pipes import update_pipes
from collisions import check_collision
from high_score import update_high_score

def update(delta_time):
    """Atualiza o estado completo do jogo a cada frame."""

    current_time = time.time() # Pega o tempo atual uma vez

    # --- Atualização da Animação do Pássaro ---
    if config.bird_texture_id and config.bird_frames_uv:
        if current_time - config.last_frame_time > config.BIRD_ANIMATION_SPEED:
            config.bird_current_frame = (config.bird_current_frame + 1) % len(config.bird_frames_uv)
            config.last_frame_time = current_time

    # --- ATUALIZA ANIMAÇÃO DOS POWER-UPS (com Ping-Pong) ---
    if config.game_started and not config.game_over:
        for powerup in config.powerups:
             if powerup.type in config.powerup_data:
                pu_data = config.powerup_data[powerup.type]
                num_frames = len(pu_data['uvs'])
                is_ping_pong = pu_data.get('ping_pong', False) # Pega config ping_pong

                # Só anima se houver múltiplos frames
                if num_frames > 1:
                    if current_time - powerup.last_frame_time > config.POWERUP_ANIMATION_SPEED:
                        if is_ping_pong:
                            # Lógica Ping-Pong
                            powerup.current_frame += powerup.animation_direction

                            # Verifica limites e inverte direção
                            if powerup.current_frame >= num_frames - 1:
                                powerup.current_frame = num_frames - 1 # Garante que não ultrapassa
                                powerup.animation_direction = -1 # Inverte para voltar
                            elif powerup.current_frame <= 0:
                                powerup.current_frame = 0 # Garante que não fica negativo
                                powerup.animation_direction = 1 # Inverte para avançar
                        else:
                            # Lógica de Loop Normal (apenas incrementa, módulo feito no desenho)
                            powerup.current_frame += 1

                        powerup.last_frame_time = current_time # Atualiza timer do frame
    # --- FIM ANIMAÇÃO POWER-UPS ---


    # --- Lógica Principal do Jogo ---
    if not config.game_started or config.game_over:
        if config.game_over:
            update_high_score(config.score)
        return

    # --- Física do Pássaro ---
    current_gravity = config.GRAVITY
    if config.heavy_jump_active:
        current_gravity *= config.HEAVYJUMP_GRAVITY_MULTIPLIER
    config.bird_velocity += current_gravity * delta_time
    config.BIRD_Y += config.bird_velocity * delta_time

    # --- Atualização dos Canos e Power-ups (Movimento/Geração) ---
    update_pipes(delta_time)

    # --- Verificação de Colisões ---
    check_collision()

    # --- Gerenciamento de Estados ---
    # Verifica se o tempo de invulnerabilidade/boost acabou
    if config.invulnerable and current_time > config.invulnerable_time:
        config.invulnerable = False
        if config.speed_multiplier > 1.0:
            config.speed_multiplier = 1.0

    # Verifica desativação pendente do Chainsaw
    if config.chainsaw_deactivation_pending:
        bird_collision_half_w = (config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W) / 2.0
        current_size_scale = config.SHRINK_SCALE_FACTOR if config.shrink_active else 1.0
        bird_left_edge = config.BIRD_X - (bird_collision_half_w * current_size_scale)
        last_pipe = config.chainsaw_last_pipe_ref
        pipe_cleared = False
        if last_pipe is not None and last_pipe in config.pipes:
            pipe_right_edge = last_pipe['x'] + config.PIPE_WIDTH
            if bird_left_edge > pipe_right_edge:
                pipe_cleared = True
        else:
            pipe_cleared = True
        if pipe_cleared:
            config.chainsaw_active = False
            config.chainsaw_deactivation_pending = False
            config.chainsaw_last_pipe_ref = None
            print("Chainsaw effect ended (Pipe Cleared/Ref Invalid).")

    # Atualizar o high score em tempo real
    if config.score > config.high_score:
        update_high_score(config.score)

    # Verifica desativação do Heavy Jump
    if config.heavy_jump_active and current_time > config.heavy_jump_end_time:
        config.heavy_jump_active = False
        print("Heavy Jump effect ended.")

    # Verifica desativação do Shrink
    if config.shrink_active and current_time > config.shrink_end_time:
        config.shrink_active = False
        print("Shrink effect ended.")