# game_pipes.py
from OpenGL.GL import *
import config
import random
import time
from powerup import PowerUp

def draw_pipes():
    """Desenha os canos na tela."""
    glColor3f(0.0, 0.6, 0.0)
    for pipe in config.pipes:
        # Cano Superior
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], 1.0)
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, 1.0)
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['top_height'])
        glVertex2f(pipe['x'], pipe['top_height'])
        glEnd()
        # Cano Inferior
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], pipe['bottom_height'])
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height'])
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, -1.0)
        glVertex2f(pipe['x'], -1.0)
        glEnd()

def update_pipes(delta_time):
    """Atualiza canos, gera novos com altura tendendo ao centro da referência estimada e ajusta v_speed inicial."""

    min_safe_bottom_limit = -1.0 + 0.1 # Limite inferior seguro para bottom_height
    max_safe_top_limit = 1.0 - 0.1     # Limite superior seguro para top_height
    max_safe_bottom_limit_for_bottom = max_safe_top_limit - config.PIPE_GAP

    # --- Move canos existentes ---
    for pipe in config.pipes:
        pipe['x'] -= config.PIPE_SPEED * config.speed_multiplier * delta_time
        if pipe.get('v_speed', 0) != 0:
            delta_y = pipe['v_speed'] * delta_time
            new_bottom_h = pipe['bottom_height'] + delta_y
            new_top_h = new_bottom_h + config.PIPE_GAP
            # Verifica limites e inverte velocidade se necessário
            if new_bottom_h < min_safe_bottom_limit:
                new_bottom_h = min_safe_bottom_limit
                pipe['v_speed'] *= -1
            elif new_bottom_h > max_safe_bottom_limit_for_bottom:
                new_bottom_h = max_safe_bottom_limit_for_bottom
                pipe['v_speed'] *= -1

            # Recalcula top_h APÓS clamp e inversão de v_speed, se houver
            new_top_h = new_bottom_h + config.PIPE_GAP
            pipe['bottom_height'] = new_bottom_h
            pipe['top_height'] = new_top_h

    # --- Remove canos que saíram da tela ---
    config.pipes[:] = [pipe for pipe in config.pipes if pipe['x'] + config.PIPE_WIDTH > -1.0]

    # --- Gera novos canos e power-ups ---
    current_time = time.time()
    time_since_last_pipe = current_time - config.last_pipe_time
    spawn_interval_adjusted = config.PIPE_SPAWN_INTERVAL / config.speed_multiplier

    if (config.game_started and not config.game_over and
            time_since_last_pipe > spawn_interval_adjusted):

        # --- Lógica de Altura (Estimando Posição Futura e Usando Triangular) ---
        overall_min_bottom_h = -1.0 + 0.2
        overall_max_bottom_h = 1.0 - 0.2 - config.PIPE_GAP

        reference_height = 0.0 # Default para o primeiro cano
        previous_was_moving = False

        if config.pipes: # Se houver um cano anterior
            previous_pipe = config.pipes[-1]
            previous_v_speed = previous_pipe.get('v_speed', 0)
            previous_was_moving = (previous_v_speed != 0)
            time_to_estimate = spawn_interval_adjusted
            estimated_drift = previous_v_speed * time_to_estimate
            estimated_future_height = previous_pipe['bottom_height'] + estimated_drift
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
        except ValueError as e:
            print(f"Erro em random.triangular: {e}. Usando uniform.")
            if current_min_h < current_max_h:
                 bottom_pipe_h = random.uniform(current_min_h, current_max_h)
            else:
                 bottom_pipe_h = current_min_h

        top_pipe_h = bottom_pipe_h + config.PIPE_GAP
        # --- Fim Lógica de Altura ---

        # --- Atribui Velocidade Vertical ---
        pipe_v_speed = 0.0
        allow_move = True
        if config.pipes and config.pipes[-1].get('v_speed', 0) != 0:
            allow_move = False

        if allow_move and random.random() < config.PIPE_MOVE_CHANCE:
            speed = random.uniform(config.MIN_PIPE_MOVE_SPEED, config.MAX_PIPE_MOVE_SPEED)
            # Atribui velocidade inicial aleatória (magnitude e sinal)
            pipe_v_speed = random.choice([speed, -speed])

            # *** AJUSTE DA VELOCIDADE INICIAL ***
            # Se o cano spawnou abaixo da referência mas está se movendo para baixo, força para cima.
            if bottom_pipe_h < reference_height and pipe_v_speed < 0:
                # print(f"Adjusting v_speed: Spawned low ({bottom_pipe_h:.2f} < ref {reference_height:.2f}), moving down ({pipe_v_speed:.2f}). Forcing up.") # Debug
                pipe_v_speed *= -1 # Inverte para positivo
            # Se o cano spawnou acima da referência mas está se movendo para cima, força para baixo.
            elif bottom_pipe_h > reference_height and pipe_v_speed > 0:
                # print(f"Adjusting v_speed: Spawned high ({bottom_pipe_h:.2f} > ref {reference_height:.2f}), moving up ({pipe_v_speed:.2f}). Forcing down.") # Debug
                pipe_v_speed *= -1 # Inverte para negativo
            # *** FIM DO AJUSTE ***

        # --- Fim Atribuição Velocidade ---

        # --- Cria e Adiciona o Novo Cano ---
        new_pipe = {
            'x': 1.0,
            'top_height': top_pipe_h,
            'bottom_height': bottom_pipe_h,
            'scored': False,
            'v_speed': pipe_v_speed # Usa a velocidade (possivelmente ajustada)
        }
        config.pipes.append(new_pipe)

        # --- Gera Power-up (Opcional) ---
        if random.random() < 0.25:
            if config.POWERUP_TYPES:
                powerup_type = random.choice(config.POWERUP_TYPES)
                powerup_y = (bottom_pipe_h + top_pipe_h) / 2.0
                powerup_x = new_pipe['x'] + config.PIPE_WIDTH / 2.0
                config.powerups.append(PowerUp(powerup_x, powerup_y, powerup_type))

        # --- Reseta Timer ---
        config.last_pipe_time = current_time

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