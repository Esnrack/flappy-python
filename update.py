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
    if not config.game_started or config.game_over:
        return

    # --- Física do Pássaro ---
    config.bird_velocity += config.GRAVITY * delta_time
    config.BIRD_Y += config.bird_velocity * delta_time

    # --- Atualização dos Canos e Power-ups ---
    # update_pipes move canos, gera novos, move powerups, decrementa contador chainsaw e marca para desativar
    update_pipes(delta_time)

    # --- Verificação de Colisões ---
    # check_collision usa o estado ATUAL de config.chainsaw_active
    check_collision()

    # --- Gerenciamento de Estados Pós-Colisão/Powerup/Update ---
    current_time_state = time.time()

    # Verifica se o tempo de invulnerabilidade/boost acabou
    if config.invulnerable and current_time_state > config.invulnerable_time:
        config.invulnerable = False
        if config.speed_multiplier > 1.0:
            config.speed_multiplier = 1.0

    # --- VERIFICA DESATIVAÇÃO PENDENTE DO CHAINSAW ---
    if config.chainsaw_deactivation_pending:
        # Calcula a borda esquerda da hitbox do pássaro na posição atual
        bird_collision_half_w = (config.BIRD_DRAW_WIDTH * config.BIRD_COLLISION_SCALE_W) / 2.0
        bird_left_edge = config.BIRD_X - bird_collision_half_w

        last_pipe = config.chainsaw_last_pipe_ref
        pipe_cleared = False

        # Verifica se a referência ao último cano ainda é válida e se ele ainda existe na lista
        if last_pipe is not None and last_pipe in config.pipes:
            pipe_right_edge = last_pipe['x'] + config.PIPE_WIDTH
            # Verifica se a borda esquerda do pássaro passou a borda direita do cano
            if bird_left_edge > pipe_right_edge:
                pipe_cleared = True
                # print("Bird cleared the last chainsaw pipe.") # Debug
        else:
            # Se a referência é None ou o cano não está mais na lista, considera como 'cleared'
            pipe_cleared = True
            # print("Chainsaw last pipe ref invalid or gone, assuming cleared.") # Debug

        # Se o cano foi considerado limpo (horizontalmente ou por ter desaparecido)
        if pipe_cleared:
            config.chainsaw_active = False
            config.chainsaw_deactivation_pending = False
            config.chainsaw_last_pipe_ref = None # Limpa a referência
            print("Chainsaw effect ended (Pipe Cleared/Ref Invalid).")
    # --- FIM VERIFICA DESATIVAÇÃO CHAINSAW ---