import config
import time
def get_game_time():
    if not config.game_started:
        return 0.0
    if config.game_paused:
        return config.pause_start_time - config.total_pause_time
    else:
        return time.time() - config.total_pause_time