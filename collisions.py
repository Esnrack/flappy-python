import config
import time

def handle_collision():
    config.lives -= 1
    if config.lives <= 0:
        config.game_over = True
    else:
        config.BIRD_Y = 0.0
        config.bird_velocity = 0.0
        config.invulnerable = True
        config.invulnerable_time = time.time() + 2

def check_collision():
    if config.BIRD_Y - config.BIRD_SIZE < -0.9 or config.BIRD_Y + config.BIRD_SIZE > 1.0:
        if not config.invulnerable:
            handle_collision()
        return
    
    for powerup in config.powerups:
        if (not powerup.collected and
            abs(config.BIRD_X - powerup.x) < (config.BIRD_SIZE + powerup.size) and
            abs(config.BIRD_Y - powerup.y) < (config.BIRD_SIZE + powerup.size)):
            powerup.collected = True
            if powerup.type == 'life':
                config.lives = min(config.lives + 1, config.INITIAL_LIVES * 2)
            else:
                config.speed_multiplier = 2.0
                config.invulnerable = True
                config.invulnerable_time = time.time() + 3

    for pipe in config.pipes:
        if (pipe['x'] < config.BIRD_X + config.BIRD_SIZE and
            pipe['x'] + config.PIPE_WIDTH > config.BIRD_X - config.BIRD_SIZE and
            (config.BIRD_Y - config.BIRD_SIZE < pipe['bottom_height'] or
             config.BIRD_Y + config.BIRD_SIZE > pipe['top_height'])):
            if not config.invulnerable:
                handle_collision()
            return
   