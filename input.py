# input.py
import glfw
import time
import config

def key_callback(window, key, scancode, action, mods):
    """Processa eventos de teclado."""

    if action == glfw.PRESS:
        # Tecla ESPAÇO
        if key == glfw.KEY_SPACE:
            if not config.game_started:
                print("Jogo Iniciado!")
                config.game_started = True
                config.last_pipe_time = time.time()
                # Resetar estado completo ao iniciar
                config.game_over = False
                config.lives = config.INITIAL_LIVES
                config.score = 0
                config.pipes.clear()
                config.powerups.clear()
                config.BIRD_Y = 0.0
                config.bird_velocity = 0.0
                config.invulnerable = False
                config.speed_multiplier = 1.0
                # --- RESET CHAINSAW STATE ---
                config.chainsaw_active = False
                config.chainsaw_pipes_remaining = 0
                config.chainsaw_deactivation_pending = False # Reset new flag
                config.chainsaw_last_pipe_ref = None       # Reset reference
                # --- FIM RESET ---

            if config.game_started and not config.game_over:
                config.bird_velocity = config.JUMP_STRENGTH

        # Tecla R (Restart)
        if key == glfw.KEY_R and config.game_over:
            print("Jogo Reiniciado!")
            # Resetar estado completo do jogo para recomeçar
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
            # --- RESET CHAINSAW STATE ---
            config.chainsaw_active = False
            config.chainsaw_pipes_remaining = 0
            config.chainsaw_deactivation_pending = False # Reset new flag
            config.chainsaw_last_pipe_ref = None       # Reset reference
            # --- FIM RESET ---