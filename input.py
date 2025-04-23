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
                config.game_started = True; config.last_pipe_time = time.time()
                # Resetar estado completo
                config.game_over = False; config.lives = config.INITIAL_LIVES
                config.score = 0; config.pipes.clear(); config.powerups.clear()
                config.BIRD_Y = 0.0; config.bird_velocity = 0.0
                config.invulnerable = False; config.speed_multiplier = 1.0
                # Reset Chainsaw
                config.chainsaw_active = False; config.chainsaw_pipes_remaining = 0
                config.chainsaw_deactivation_pending = False; config.chainsaw_last_pipe_ref = None
                # Reset Heavy Jump
                config.heavy_jump_active = False; config.heavy_jump_end_time = 0.0
                # --- RESET SHRINK STATE ---
                config.shrink_active = False; config.shrink_end_time = 0.0
                # --- FIM RESET ---

            if config.game_started and not config.game_over:
                current_jump_strength = config.JUMP_STRENGTH
                if config.heavy_jump_active: current_jump_strength *= config.HEAVYJUMP_JUMP_MULTIPLIER
                config.bird_velocity = current_jump_strength

        # Tecla R (Restart)
        if key == glfw.KEY_R and config.game_over:
            print("Jogo Reiniciado!")
            # Resetar estado completo
            config.game_over = False; config.game_started = False
            config.lives = config.INITIAL_LIVES; config.score = 0
            config.pipes.clear(); config.powerups.clear()
            config.BIRD_Y = 0.0; config.bird_velocity = 0.0
            config.invulnerable = False; config.speed_multiplier = 1.0
            config.last_pipe_time = 0
            # Reset Chainsaw
            config.chainsaw_active = False; config.chainsaw_pipes_remaining = 0
            config.chainsaw_deactivation_pending = False; config.chainsaw_last_pipe_ref = None
            # Reset Heavy Jump
            config.heavy_jump_active = False; config.heavy_jump_end_time = 0.0
            # --- RESET SHRINK STATE ---
            config.shrink_active = False; config.shrink_end_time = 0.0
            # --- FIM RESET ---