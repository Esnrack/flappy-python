from OpenGL.GL import *
import config
import random
import time

def draw_pipes():
    for pipe in config.pipes:
        glColor3f(0.0, 0.8, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], 1.0)
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, 1.0)
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['top_height'])
        glVertex2f(pipe['x'], pipe['top_height'])
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], pipe['bottom_height'])
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height'])
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, -1.0)
        glVertex2f(pipe['x'], -1.0)
        glEnd()

def update_pipes(delta_time):
    for pipe in config.pipes:
        pipe['x'] -= config.PIPE_SPEED * config.speed_multiplier * delta_time

    config.pipes[:] = [pipe for pipe in config.pipes if pipe['x'] + config.PIPE_WIDTH > -1.0]

    current_time = time.time()
    if (current_time - config.last_pipe_time >
            config.PIPE_SPAWN_INTERVAL / config.speed_multiplier and
            config.game_started and not config.game_over):
        height = random.uniform(0.2, 0.6)
        config.pipes.append({
            'x': 1.0,
            'top_height': height + config.PIPE_GAP,
            'bottom_height': height
        })

        if random.random() < 0.2:
            from powerup import PowerUp  # Import local para evitar dependência circular
            powerup_type = 'life' if random.random() < 0.7 else 'speed'
            config.powerups.append(PowerUp(
                1.0,
                random.uniform(-0.7, 0.7),
                powerup_type
            ))

        config.last_pipe_time = current_time
        config.score += 1

    # Atualiza a posição dos power-ups
    for powerup in config.powerups:
        powerup.x -= config.PIPE_SPEED * config.speed_multiplier * delta_time

    config.powerups[:] = [p for p in config.powerups if not (p.x + p.size < -1.0 or p.collected)]
