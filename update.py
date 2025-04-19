# update.py
import config
import time
from game_pipes import update_pipes
from collisions import check_collision

def update(delta_time):
    """Atualiza o estado completo do jogo a cada frame."""

    # --- Atualização da Animação do Pássaro ---
    current_time_anim = time.time()
    if config.bird_texture_id and config.bird_frames_uv:
        if current_time_anim - config.last_frame_time > config.BIRD_ANIMATION_SPEED:
            config.bird_current_frame = (config.bird_current_frame + 1) % len(config.bird_frames_uv)
            config.last_frame_time = current_time_anim

    # --- Lógica Principal do Jogo ---
    if not config.game_started or config.game_over: return

    # --- Física do Pássaro ---
    current_gravity = config.GRAVITY
    if config.heavy_jump_active: current_gravity *= config.HEAVYJUMP_GRAVITY_MULTIPLIER
    config.bird_velocity += current_gravity * delta_time
    config.BIRD_Y += config.bird_velocity * delta_time

    # --- Atualização dos Canos e Power-ups ---
    update_pipes(delta_time)

    # --- Verificação de Colisões ---
    check_collision()

    # --- Gerenciamento de Estados Pós-Colisão/Powerup/Update ---
    current_time_state = time.time()

    # Verifica se o tempo de invulnerabilidade/boost acabou
    if config.invulnerable and current_time_state > config.invulnerable_time:
        config.invulnerable = False
        if config.speed_multiplier > 1.0: config.speed_multiplier = 1.0

    # Verifica desativação pendente do Chainsaw
    if config.chainsaw_deactivation_pending:
        bird_collision_half_w = (config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W) / 2.0
        # Aplica shrink aqui também para o cálculo da borda esquerda
        current_size_scale = config.SHRINK_SCALE_FACTOR if config.shrink_active else 1.0
        bird_left_edge = config.BIRD_X - (bird_collision_half_w * current_size_scale)
        last_pipe = config.chainsaw_last_pipe_ref
        pipe_cleared = False
        if last_pipe is not None and last_pipe in config.pipes:
            pipe_right_edge = last_pipe['x'] + config.PIPE_WIDTH
            if bird_left_edge > pipe_right_edge: pipe_cleared = True
        else: pipe_cleared = True
        if pipe_cleared:
            config.chainsaw_active = False; config.chainsaw_deactivation_pending = False
            config.chainsaw_last_pipe_ref = None; print("Chainsaw effect ended (Pipe Cleared/Ref Invalid).")

    # Verifica desativação do Heavy Jump
    if config.heavy_jump_active and current_time_state > config.heavy_jump_end_time:
        config.heavy_jump_active = False; print("Heavy Jump effect ended.")

    # --- VERIFICA DESATIVAÇÃO DO SHRINK ---
    if config.shrink_active and current_time_state > config.shrink_end_time:
        config.shrink_active = False
        print("Shrink effect ended.")
    # --- FIM VERIFICA DESATIVAÇÃO SHRINK ---