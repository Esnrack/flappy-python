import config
import time

def get_game_time():
    if not config.game_started:
        return 0.0

    current_real_time = time.time()

    if config.game_paused:
        return config.pause_start_time - config.total_pause_duration
    else:
        return current_real_time - config.total_pause_duration