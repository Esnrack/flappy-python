# game_pipes.py
from OpenGL.GL import *
import config
import random
import time
from powerup import PowerUp

def draw_pipes():
    """Desenha os canos na tela, ajustando visualmente o gap se chainsaw ativo."""
    glColor3f(0.0, 0.6, 0.0) # Verde escuro
    for pipe in config.pipes:
        # --- AJUSTE VISUAL CHAINSAW ---
        # Calcula o gap EFETIVO para este cano baseado no estado global
        current_gap = config.PIPE_GAP
        if config.chainsaw_active:
            current_gap += config.CHAINSAW_GAP_INCREASE
        # Calcula a altura superior VISUAL/DE COLISÃO
        actual_top_height = pipe['bottom_height'] + current_gap
        # --- FIM AJUSTE VISUAL ---

        # Cano Superior - Usa actual_top_height para desenhar
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], 1.0) # Top-Left da tela
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, 1.0) # Top-Right da tela
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, actual_top_height) # Bottom-Right do cano superior
        glVertex2f(pipe['x'], actual_top_height) # Bottom-Left do cano superior
        glEnd()

        # Cano Inferior - Desenha normalmente baseado em bottom_height
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], pipe['bottom_height']) # Top-Left do cano inferior
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height']) # Top-Right do cano inferior
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, -1.0) # Bottom-Right da tela
        glVertex2f(pipe['x'], -1.0) # Bottom-Left da tela
        glEnd()

def update_pipes(delta_time):
    """Atualiza canos, gera novos, e gera powerups entre canos em zona alcançável."""

    min_safe_bottom_limit = -1.0 + 0.1
    max_safe_top_limit = 1.0 - 0.1
    # Usa GAP NORMAL para calcular limites estruturais de movimento
    max_safe_bottom_limit_for_bottom = max_safe_top_limit - config.PIPE_GAP

    # --- Move canos existentes ---
    for pipe in config.pipes:
        pipe['x'] -= config.PIPE_SPEED * config.speed_multiplier * delta_time
        if pipe.get('v_speed', 0) != 0:
            delta_y = pipe['v_speed'] * delta_time
            new_bottom_h = pipe['bottom_height'] + delta_y
            if new_bottom_h < min_safe_bottom_limit:
                new_bottom_h = min_safe_bottom_limit
                pipe['v_speed'] *= -1
            elif new_bottom_h > max_safe_bottom_limit_for_bottom: # Usa limite estrutural
                new_bottom_h = max_safe_bottom_limit_for_bottom
                pipe['v_speed'] *= -1
            pipe['bottom_height'] = new_bottom_h
            # A altura superior ARMAZENADA representa o topo ESTRUTURAL
            pipe['top_height'] = new_bottom_h + config.PIPE_GAP


    # --- Remove canos que saíram da tela ---
    config.pipes[:] = [pipe for pipe in config.pipes if pipe['x'] + config.PIPE_WIDTH > -1.0]

    # --- Gera novos canos ---
    current_time = time.time()
    time_since_last_pipe = current_time - config.last_pipe_time
    spawn_interval_adjusted = config.PIPE_SPAWN_INTERVAL / config.speed_multiplier

    pipe_generated_this_frame = False

    if (config.game_started and not config.game_over and
            time_since_last_pipe > spawn_interval_adjusted):

        # --- Lógica de Altura do Cano (Calcula bottom_pipe_h) ---
        overall_min_bottom_h = -1.0 + 0.2
        overall_max_bottom_h = 1.0 - 0.2 - config.PIPE_GAP # Baseado no gap normal
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

        if previous_was_moving: height_change_limit = config.MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING
        else: height_change_limit = config.MAX_PIPE_HEIGHT_CHANGE
        target_min = reference_height - height_change_limit
        target_max = reference_height + height_change_limit
        current_min_h = max(overall_min_bottom_h, target_min)
        current_max_h = min(overall_max_bottom_h, target_max)
        if current_min_h > current_max_h: current_min_h = current_max_h = reference_height
        mode = max(current_min_h, min(current_max_h, reference_height))
        try:
            if current_min_h < current_max_h: bottom_pipe_h = random.triangular(current_min_h, current_max_h, mode)
            else: bottom_pipe_h = current_min_h
        except ValueError: bottom_pipe_h = random.uniform(current_min_h, current_max_h) if current_min_h < current_max_h else current_min_h

        # Calcula o gap EFETIVO para este NOVO cano
        current_gap = config.PIPE_GAP
        if config.chainsaw_active:
            current_gap += config.CHAINSAW_GAP_INCREASE
        # Calcula e armazena a altura superior baseada no gap efetivo
        top_pipe_h = bottom_pipe_h + current_gap
        # --- Fim Lógica de Altura do Cano ---

        # --- Atribui Velocidade Vertical do Cano ---
        pipe_v_speed = 0.0
        allow_move = True
        if config.pipes and config.pipes[-1].get('v_speed', 0) != 0: allow_move = False
        if allow_move and random.random() < config.PIPE_MOVE_CHANCE:
            speed = random.uniform(config.MIN_PIPE_MOVE_SPEED, config.MAX_PIPE_MOVE_SPEED)
            pipe_v_speed = random.choice([speed, -speed])
            if bottom_pipe_h < reference_height and pipe_v_speed < 0: pipe_v_speed *= -1
            elif bottom_pipe_h > reference_height and pipe_v_speed > 0: pipe_v_speed *= -1
        # --- Fim Atribuição Velocidade ---

        # --- Cria e Adiciona o Novo Cano ---
        # As alturas armazenadas (bottom_pipe_h, top_pipe_h) refletem o gap efetivo no momento da criação
        new_pipe = { 'x': 1.0, 'top_height': top_pipe_h, 'bottom_height': bottom_pipe_h, 'scored': False, 'v_speed': pipe_v_speed }
        config.pipes.append(new_pipe)
        pipe_generated_this_frame = True
        config.last_pipe_time = current_time

    # --- Gera Power-up (Opcional - ENTRE Canos) ---
    if pipe_generated_this_frame and len(config.pipes) >= 2:
        previous_pipe = config.pipes[-2]
        newly_created_pipe = config.pipes[-1]

        # --- VALOR ALTERADO ---
        if random.random() < 0.10: # Era 0.05
            if config.POWERUP_TYPES:
                powerup_type = random.choice(config.POWERUP_TYPES)
                prev_right_edge = previous_pipe['x'] + config.PIPE_WIDTH
                new_left_edge = newly_created_pipe['x']
                powerup_x = (prev_right_edge + new_left_edge) / 2.0

                # Calcula Y baseado no caminho entre os centros das aberturas
                # Usa as alturas ARMAZENADAS dos canos para calcular os centros
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


    # --- Atualiza e Remove Power-ups ---
    for powerup in config.powerups:
        powerup.x -= config.PIPE_SPEED * config.speed_multiplier * delta_time
    config.powerups[:] = [p for p in config.powerups if not p.collected and (p.x + p.collision_size > -1.0)]


    # --- Lógica de Pontuação ---
    for pipe in config.pipes:
         pipe_right_edge = pipe['x'] + config.PIPE_WIDTH
         if not pipe.get('scored', False) and config.BIRD_X > pipe_right_edge:
              config.score += 1
              pipe['scored'] = True
              # print(f"Pontuação: {config.score}") # Debug

              # --- ATUALIZA CONTAGEM DO CHAINSAW ---
              # Só decrementa se a desativação NÃO estiver pendente (evita decrementar múltiplas vezes)
              if config.chainsaw_active and not config.chainsaw_deactivation_pending:
                  config.chainsaw_pipes_remaining -= 1
                  # print(f"Chainsaw: {config.chainsaw_pipes_remaining} pipes left.") # Debug
                  # Se a contagem chegou a zero, marca para desativar e guarda a referência
                  if config.chainsaw_pipes_remaining <= 0:
                      config.chainsaw_deactivation_pending = True
                      config.chainsaw_last_pipe_ref = pipe