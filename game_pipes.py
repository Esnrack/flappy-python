# game_pipes.py
from OpenGL.GL import *
import config
import random
import time
from powerup import PowerUp

# --- draw_pipes (como na versão anterior, com cálculo de repetição) ---
def draw_pipes(use_fallback_color=False):
    trunk_ok = config.trunk_texture_id is not None and config.trunk_image_height > 0
    root_ok = config.root_texture_id is not None and config.root_image_height > 0
    textures_loaded_successfully = trunk_ok and root_ok
    if use_fallback_color or not textures_loaded_successfully:
        glColor3f(0.0, 0.6, 0.0)
        use_fallback_color = True
    root_world_height = 0.0
    root_world_width = 0.0
    if root_ok and config.WINDOW_HEIGHT > 0 :
        world_height_per_pixel = 2.0 / config.WINDOW_HEIGHT
        root_world_height = config.ROOT_SPRITE_HEIGHT_PX * world_height_per_pixel
        if config.root_aspect_ratio > 0:
            root_world_width = root_world_height * config.root_aspect_ratio
        else:
            root_world_width = config.PIPE_WIDTH
        root_world_width *= config.ROOT_DRAW_WIDTH_SCALE
    U0, V0 = 0.0, 0.0
    U1, V1 = 1.0, 1.0
    trunk_aspect = 1.0
    if trunk_ok and config.trunk_image_height > 0:
        trunk_aspect = config.trunk_image_width / config.trunk_image_height
    for pipe in config.pipes:
        current_gap = config.PIPE_GAP
        is_chainsaw_effective = config.chainsaw_active or \
                                (config.chainsaw_deactivation_pending and config.chainsaw_last_pipe_ref == pipe)
        if is_chainsaw_effective:
            current_gap += config.CHAINSAW_GAP_INCREASE
        actual_top_height = pipe['bottom_height'] + current_gap
        ground_y = -0.9
        # Desenha Cano Superior
        if not use_fallback_color:
            glBindTexture(GL_TEXTURE_2D, config.trunk_texture_id)
            glBegin(GL_QUADS)
            bottom_left_v_top = (pipe['x'], actual_top_height)
            bottom_right_v_top = (pipe['x'] + config.PIPE_WIDTH, actual_top_height)
            top_right_v_top = (pipe['x'] + config.PIPE_WIDTH, 1.0)
            top_left_v_top = (pipe['x'], 1.0)
            tex_v_at_gap = V0
            pipe_visual_height_t = 1.0 - actual_top_height
            one_tile_world_height = config.PIPE_WIDTH / trunk_aspect if trunk_aspect > 0 else config.PIPE_WIDTH
            v_repeats_t = pipe_visual_height_t / one_tile_world_height if one_tile_world_height > 0 else 1.0
            tex_v_at_limit = V0 + v_repeats_t * (V1 - V0)
            glTexCoord2f(U0, tex_v_at_gap)
            glVertex2f(*bottom_left_v_top)
            glTexCoord2f(U1, tex_v_at_gap)
            glVertex2f(*bottom_right_v_top)
            glTexCoord2f(U1, tex_v_at_limit)
            glVertex2f(*top_right_v_top)
            glTexCoord2f(U0, tex_v_at_limit)
            glVertex2f(*top_left_v_top)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glVertex2f(pipe['x'], actual_top_height)
            glVertex2f(pipe['x'] + config.PIPE_WIDTH, actual_top_height)
            glVertex2f(pipe['x'] + config.PIPE_WIDTH, 1.0)
            glVertex2f(pipe['x'], 1.0)
            glEnd()
        # Desenha Cano Inferior (Tronco)
        if not use_fallback_color:
            glBindTexture(GL_TEXTURE_2D, config.trunk_texture_id)
            glBegin(GL_QUADS)
            bottom_left_v_trunk = (pipe['x'], ground_y)
            bottom_right_v_trunk = (pipe['x'] + config.PIPE_WIDTH, ground_y)
            top_right_v_trunk = (pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height'])
            top_left_v_trunk = (pipe['x'], pipe['bottom_height'])
            tex_v_at_gap = V0
            pipe_visual_height_b = pipe['bottom_height'] - ground_y
            one_tile_world_height = config.PIPE_WIDTH / trunk_aspect if trunk_aspect > 0 else config.PIPE_WIDTH
            v_repeats_b = pipe_visual_height_b / one_tile_world_height if one_tile_world_height > 0 else 1.0
            tex_v_at_limit = V0 + v_repeats_b * (V1 - V0)
            glTexCoord2f(U0, tex_v_at_limit)
            glVertex2f(*bottom_left_v_trunk)
            glTexCoord2f(U1, tex_v_at_limit)
            glVertex2f(*bottom_right_v_trunk)
            glTexCoord2f(U1, tex_v_at_gap)
            glVertex2f(*top_right_v_trunk)
            glTexCoord2f(U0, tex_v_at_gap)
            glVertex2f(*top_left_v_trunk)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glVertex2f(pipe['x'], ground_y)
            glVertex2f(pipe['x'] + config.PIPE_WIDTH, ground_y)
            glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height'])
            glVertex2f(pipe['x'], pipe['bottom_height'])
            glEnd()
        # Desenha Base com Raízes
        if not use_fallback_color and root_ok:
            glBindTexture(GL_TEXTURE_2D, config.root_texture_id)
            glBegin(GL_QUADS)
            center_x = pipe['x'] + config.PIPE_WIDTH / 2.0
            half_root_w = root_world_width / 2.0
            x_left_root = center_x - half_root_w
            x_right_root = center_x + half_root_w
            y_bottom_root = ground_y
            y_top_root = ground_y + root_world_height
            glTexCoord2f(U0, V1)
            glVertex2f(x_left_root, y_bottom_root)
            glTexCoord2f(U1, V1)
            glVertex2f(x_right_root, y_bottom_root)
            glTexCoord2f(U1, V0)
            glVertex2f(x_right_root, y_top_root)
            glTexCoord2f(U0, V0)
            glVertex2f(x_left_root, y_top_root)
            glEnd()
    if not use_fallback_color and textures_loaded_successfully:
        glBindTexture(GL_TEXTURE_2D, 0)
    elif use_fallback_color:
        glColor3f(1.0, 1.0, 1.0)

# --- update_pipes ---
def update_pipes(delta_time):
    min_safe_bottom_limit = -1.0 + 0.1
    max_safe_top_limit = 1.0 - 0.1
    max_safe_bottom_limit_for_bottom = max_safe_top_limit - config.PIPE_GAP
    for pipe in config.pipes:
        # Move canos
        pipe['x'] -= config.PIPE_SPEED * config.speed_multiplier * delta_time
        if pipe.get('v_speed', 0) != 0:
            delta_y = pipe['v_speed'] * delta_time
            new_bottom_h = pipe['bottom_height'] + delta_y
            max_bottom_limit_struct = max_safe_top_limit - config.PIPE_GAP
            if new_bottom_h < min_safe_bottom_limit:
                new_bottom_h = min_safe_bottom_limit
                pipe['v_speed'] *= -1
            elif new_bottom_h > max_bottom_limit_struct:
                new_bottom_h = max_bottom_limit_struct
                pipe['v_speed'] *= -1
            pipe['bottom_height'] = new_bottom_h
            pipe['top_height'] = new_bottom_h + config.PIPE_GAP
    config.pipes[:] = [pipe for pipe in config.pipes if pipe['x'] + config.PIPE_WIDTH > -1.0] # Remove canos
    current_time = time.time()
    time_since_last_pipe = current_time - config.last_pipe_time # Gera novos
    spawn_interval_adjusted = config.PIPE_SPAWN_INTERVAL / config.speed_multiplier
    pipe_generated_this_frame = False
    if (config.game_started and not config.game_over and time_since_last_pipe > spawn_interval_adjusted):
        overall_min_bottom_h = -1.0 + 0.2
        overall_max_bottom_h = 1.0 - 0.2 - config.PIPE_GAP
        reference_height = 0.0
        previous_was_moving = False
        if config.pipes:
            previous_pipe_ref = config.pipes[-1]
            previous_v_speed_ref = previous_pipe_ref.get('v_speed', 0)
            previous_was_moving = (previous_v_speed_ref != 0)
            time_to_estimate = spawn_interval_adjusted
            estimated_drift = previous_v_speed_ref * time_to_estimate
            estimated_future_height = previous_pipe_ref['bottom_height'] + estimated_drift
            reference_height = max(overall_min_bottom_h, min(overall_max_bottom_h, estimated_future_height))
        else:
            reference_height = (overall_max_bottom_h + overall_min_bottom_h) / 2 - 0.1
        if previous_was_moving:
            height_change_limit = config.MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING
        else:
            height_change_limit = config.MAX_PIPE_HEIGHT_CHANGE
        target_min = reference_height - height_change_limit
        target_max = reference_height + height_change_limit
        current_min_h = max(overall_min_bottom_h, target_min)
        current_max_h = min(overall_max_bottom_h, target_max)
        if current_min_h > current_max_h:
            current_min_h = current_max_h = reference_height
        mode = max(current_min_h, min(current_max_h, reference_height))
        try:
            if current_min_h < current_max_h:
                bottom_pipe_h = random.triangular(current_min_h, current_max_h, mode)
            else:
                bottom_pipe_h = current_min_h
        except ValueError:
            bottom_pipe_h = random.uniform(current_min_h, current_max_h) if current_min_h < current_max_h else current_min_h
        current_gap = config.PIPE_GAP
        if config.chainsaw_active:
            current_gap += config.CHAINSAW_GAP_INCREASE
        top_pipe_h_structural = bottom_pipe_h + config.PIPE_GAP
        pipe_v_speed = 0.0
        allow_move = True
        if config.pipes and config.pipes[-1].get('v_speed', 0) != 0:
            allow_move = False
        if allow_move and random.random() < config.PIPE_MOVE_CHANCE:
            speed = random.uniform(config.MIN_PIPE_MOVE_SPEED, config.MAX_PIPE_MOVE_SPEED)
            pipe_v_speed = random.choice([speed, -speed])
            if bottom_pipe_h < reference_height and pipe_v_speed < 0:
                pipe_v_speed *= -1
            elif bottom_pipe_h > reference_height and pipe_v_speed > 0:
                pipe_v_speed *= -1
        new_pipe = { 'x': 1.0, 'top_height': top_pipe_h_structural, 'bottom_height': bottom_pipe_h, 'scored': False, 'v_speed': pipe_v_speed }
        config.pipes.append(new_pipe)
        pipe_generated_this_frame = True
        config.last_pipe_time = current_time
    if pipe_generated_this_frame and len(config.pipes) >= 2: # Gera Powerup
        previous_pipe = config.pipes[-2]
        newly_created_pipe = config.pipes[-1]
        if random.random() < 0.10:
            # --- Seleciona tipo de powerup da nova config ---
            available_pu_types = list(config.powerup_data.keys()) # Obtem tipos carregados
            if available_pu_types:
                powerup_type = random.choice(available_pu_types)
            # --- Fim Seleção ---
                prev_right_edge = previous_pipe['x'] + config.PIPE_WIDTH
                new_left_edge = newly_created_pipe['x']
                powerup_x = (prev_right_edge + new_left_edge) / 2.0
                prev_gap_center_y = (previous_pipe['bottom_height'] + previous_pipe['top_height']) / 2.0
                new_gap_center_y = (newly_created_pipe['bottom_height'] + newly_created_pipe['top_height']) / 2.0
                path_midpoint_y = (prev_gap_center_y + new_gap_center_y) / 2.0
                half_range = config.POWERUP_Y_RANGE_AROUND_PATH / 2.0
                powerup_y_min = path_midpoint_y - half_range
                powerup_y_max = path_midpoint_y + half_range
                powerup_y = random.uniform(powerup_y_min, powerup_y_max)
                min_y_bound = -1.0 + config.POWERUP_DRAW_SIZE * 0.5
                max_y_bound = 1.0 - config.POWERUP_DRAW_SIZE * 0.5
                powerup_y = max(min_y_bound, min(max_y_bound, powerup_y))
                config.powerups.append(PowerUp(powerup_x, powerup_y, powerup_type))
    for powerup in config.powerups: # Atualiza powerups
        powerup.x -= config.PIPE_SPEED * config.speed_multiplier * delta_time
    config.powerups[:] = [p for p in config.powerups if not p.collected and (p.x + p.collision_size > -1.0)]
    for pipe in config.pipes: # Pontuação
         pipe_right_edge = pipe['x'] + config.PIPE_WIDTH
         if not pipe.get('scored', False) and config.BIRD_X > pipe_right_edge:
              config.score += 1
              pipe['scored'] = True
              if config.chainsaw_active and not config.chainsaw_deactivation_pending:
                  config.chainsaw_pipes_remaining -= 1
                  if config.chainsaw_pipes_remaining <= 0:
                      config.chainsaw_deactivation_pending = True
                      config.chainsaw_last_pipe_ref = pipe