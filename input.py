import glfw
import time
import config

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            if not config.game_started:
                config.game_started = True
                config.last_pipe_time = time.time()
            if not config.game_over:
                config.bird_velocity = config.JUMP_STRENGTH

        if key == glfw.KEY_R and config.game_over:
            config.game_over = False
            config.game_started = False
            config.lives = config.INITIAL_LIVES
            config.score = 0
            config.pipes.clear()
            config.powerups.clear()
            config.BIRD_Y = 0.0
            config.bird_velocity = 0.0
            config.invulnerable = False
            config.speed_multiplier = 1.0
            config.last_pipe_time = 0
