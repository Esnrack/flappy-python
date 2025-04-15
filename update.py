import config
import time
from game_pipes import update_pipes
from collisions import check_collision

def update(delta_time):
    if not config.game_started or config.game_over:
        return

    config.bird_velocity += config.GRAVITY * delta_time
    config.BIRD_Y += config.bird_velocity * delta_time
    update_pipes(delta_time)
    check_collision()

    current_time = time.time()
    if config.invulnerable and current_time > config.invulnerable_time:
        config.invulnerable = False
        if config.speed_multiplier > 1.0:
            config.speed_multiplier = 1.0
