# update.py
import config # Importa config
import time
import random # Para spawn de nuvens
from game_pipes import update_pipes # Atualiza canos (posição, geração, remoção) e powerups (posição, remoção)
from collisions import check_collision # Verifica colisões
from high_score import update_high_score
from clouds import Cloud
# --- REMOVIDO Import de main ---
# from main import world_x_min, world_x_max
# --- FIM REMOÇÃO ---

def update(delta_time):
    """Atualiza o estado completo do jogo a cada frame."""

    # --- Atualização da Animação do Pássaro ---
    current_time_anim = time.time()
    if config.bird_texture_id and config.bird_frames_uv:
        if current_time_anim - config.last_frame_time > config.BIRD_ANIMATION_SPEED:
            config.bird_current_frame = (config.bird_current_frame + 1) % len(config.bird_frames_uv)
            config.last_frame_time = current_time_anim

    # Animação Power-ups
    if config.game_started and not config.game_over:
        for powerup in config.powerups:
             if powerup.type in config.powerup_data:
                pu_data = config.powerup_data[powerup.type]
                num_frames = len(pu_data['uvs']); is_ping_pong = pu_data.get('ping_pong', False)
                if num_frames > 1:
                    if current_time_anim - powerup.last_frame_time > config.POWERUP_ANIMATION_SPEED:
                        if is_ping_pong:
                            powerup.current_frame += powerup.animation_direction
                            if powerup.current_frame >= num_frames - 1: powerup.current_frame = num_frames - 1; powerup.animation_direction = -1
                            elif powerup.current_frame <= 0: powerup.current_frame = 0; powerup.animation_direction = 1
                        else: powerup.current_frame += 1
                        powerup.last_frame_time = current_time_anim

    # Atualiza Nuvens
    if config.game_started and not config.game_over:
        # Spawn
        if current_time_anim - config.last_cloud_spawn_time > config.next_cloud_spawn_interval:
            cloud_y = random.uniform(config.CLOUD_Y_MIN, config.CLOUD_Y_MAX)
            cloud_speed = random.uniform(config.CLOUD_SPEED_MIN, config.CLOUD_SPEED_MAX)
            cloud_scale = random.uniform(config.CLOUD_SCALE_MIN, config.CLOUD_SCALE_MAX)
            cloud_sprite_path = None
            if config.CLOUD_CONFIG:
                 chosen_config = random.choice(config.CLOUD_CONFIG)
                 cloud_sprite_path = chosen_config['path']
            new_cloud = Cloud(cloud_y, cloud_sprite_path, cloud_speed, cloud_scale)
            # Usa config.world_x_max para spawn inicial
            new_cloud.x = config.world_x_max + (new_cloud.get_draw_dimensions()[0] / 2.0) + 0.1
            config.clouds.append(new_cloud)
            config.last_cloud_spawn_time = current_time_anim
            config.next_cloud_spawn_interval = random.uniform(config.CLOUD_SPAWN_INTERVAL_MIN, config.CLOUD_SPAWN_INTERVAL_MAX)

        # Move, Anima, Despawn
        clouds_to_keep = []
        for cloud in config.clouds:
            cloud.x -= cloud.speed * delta_time * config.speed_multiplier
            if cloud.sprite_path and cloud.sprite_path in config.cloud_data:
                cloud_info = config.cloud_data[cloud.sprite_path]
                num_frames = len(cloud_info['uvs'])
                if num_frames > 1:
                    if current_time_anim - cloud.last_frame_time > config.CLOUD_ANIMATION_SPEED:
                        cloud.current_frame = (cloud.current_frame + 1) # Loop simples
                        cloud.last_frame_time = current_time_anim
            cloud_draw_w, _ = cloud.get_draw_dimensions()
            cloud_right_edge = cloud.x + cloud_draw_w / 2.0
            # Usa config.world_x_min para despawn
            if cloud_right_edge > config.world_x_min - 0.1:
                 clouds_to_keep.append(cloud)
        config.clouds = clouds_to_keep

    # Lógica Principal do Jogo
    if not config.game_started or config.game_over:
        if config.game_over: update_high_score(config.score)
        return

    # Física Pássaro
    current_gravity = config.GRAVITY
    if config.heavy_jump_active: current_gravity *= config.HEAVYJUMP_GRAVITY_MULTIPLIER
    config.bird_velocity += current_gravity * delta_time
    config.BIRD_Y += config.bird_velocity * delta_time

    # --- Atualização dos Canos e Power-ups (Movimento/Geração) ---
    update_pipes(delta_time)

    # Offset Chão
    if config.GROUND_TILE_WORLD_WIDTH > 0:
        scroll_speed_uv = (config.PIPE_SPEED * config.speed_multiplier) / config.GROUND_TILE_WORLD_WIDTH
        config.ground_offset_x += scroll_speed_uv * delta_time
        config.ground_offset_x %= 1.0

    # Colisões
    check_collision()

    # --- Gerenciamento de Estados Pós-Colisão/Powerup/Update ---
    current_time_state = config.get_game_time()

    # Verifica se o tempo de invulnerabilidade/boost acabou
    if config.invulnerable and current_time_state > config.invulnerable_time:
        config.invulnerable = False
        if config.speed_multiplier > 1.0: config.speed_multiplier = 1.0

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
            config.chainsaw_last_pipe_ref = None; print("Chainsaw effect ended.")

    if config.score > config.high_score: update_high_score(config.score)

    # Verifica desativação do Heavy Jump
    if config.heavy_jump_active and current_time_state > config.heavy_jump_end_time:
        config.heavy_jump_active = False; print("Heavy Jump effect ended.")

    # --- VERIFICA DESATIVAÇÃO DO SHRINK ---
    if config.shrink_active and current_time_state > config.shrink_end_time:
        config.shrink_active = False
        print("Shrink effect ended.")
    # --- FIM VERIFICA DESATIVAÇÃO SHRINK ---