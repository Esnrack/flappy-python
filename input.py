import glfw
import time
import config
import random
import pause

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            if config.game_started and not config.game_over:
                if not config.game_paused:
                    config.game_paused = True
                    config.pause_start_time = time.time()
                    print("Jogo pausado!")
                else:
                    config.game_paused = False
                    pause_duration = time.time() - config.pause_start_time
                    config.total_pause_duration += pause_duration

                    if config.invulnerable_time > config.pause_start_time:
                        config.invulnerable_time += pause_duration
                    if config.heavy_jump_end_time > config.pause_start_time:
                        config.heavy_jump_end_time += pause_duration
                    if config.shrink_end_time > config.pause_start_time:
                        config.shrink_end_time += pause_duration

                    config.last_pipe_time += pause_duration
                    config.last_cloud_spawn_time += pause_duration

                    config.last_frame_time += pause_duration
                    for powerup in config.powerups:
                         powerup.last_frame_time += pause_duration
                    for cloud in config.clouds:
                         cloud.last_frame_time += pause_duration


                    print(f"Jogo continuado! (Pausado por {pause_duration:.1f}s)")

        if key == glfw.KEY_SPACE:
            if config.game_paused:
                return

            if not config.game_started:
                print("Jogo Iniciado!")
                config.game_started = True
                current_game_time = pause.get_game_time()
                config.last_pipe_time = current_game_time
                config.last_cloud_spawn_time = current_game_time
                config.next_cloud_spawn_interval = random.uniform(config.CLOUD_SPAWN_INTERVAL_MIN, config.CLOUD_SPAWN_INTERVAL_MAX)
                config.last_frame_time = time.time()

                config.game_over = False
                config.lives = config.INITIAL_LIVES
                config.score = 0
                config.pipes.clear()
                config.powerups.clear()
                config.BIRD_Y = 0.0
                config.bird_velocity = 0.0
                config.invulnerable = False
                config.speed_multiplier = 1.0
                config.chainsaw_active = False
                config.chainsaw_pipes_remaining = 0
                config.chainsaw_deactivation_pending = False
                config.chainsaw_last_pipe_ref = None
                config.heavy_jump_active = False
                config.heavy_jump_end_time = 0.0
                config.shrink_active = False
                config.shrink_end_time = 0.0
                config.ground_offset_x = 0.0
                config.clouds.clear()
                config.game_paused = False
                config.pause_start_time = 0.0
                config.total_pause_duration = 0.0

            if config.game_started and not config.game_over:
                current_jump_strength = config.JUMP_STRENGTH
                if config.heavy_jump_active:
                    current_jump_strength *= config.HEAVYJUMP_JUMP_MULTIPLIER
                config.bird_velocity = current_jump_strength

        if key == glfw.KEY_R and config.game_over:
            print("Jogo Reiniciado!")
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
            config.chainsaw_active = False
            config.chainsaw_pipes_remaining = 0
            config.chainsaw_deactivation_pending = False
            config.chainsaw_last_pipe_ref = None
            config.heavy_jump_active = False
            config.heavy_jump_end_time = 0.0
            config.shrink_active = False
            config.shrink_end_time = 0.0
            config.ground_offset_x = 0.0
            config.clouds.clear()
            config.last_cloud_spawn_time = 0.0
            config.next_cloud_spawn_interval = 0.0
            config.game_paused = False
            config.pause_start_time = 0.0
            config.total_pause_duration = 0.0