# input.py
import glfw
import time
import config

def key_callback(window, key, scancode, action, mods):
    """Processa eventos de teclado."""

    if action == glfw.PRESS:
        # Tecla ESPAÇO
        if key == glfw.KEY_SPACE:
            # Inicia o jogo se ainda não começou
            if not config.game_started:
                print("Jogo Iniciado!")
                config.game_started = True
                config.last_pipe_time = time.time() # Inicia timer para o primeiro cano
                # Resetar estado completo ao iniciar pela primeira vez ou após game over sem restart
                config.game_over = False
                config.lives = config.INITIAL_LIVES
                config.score = 0
                config.pipes.clear()
                config.powerups.clear()
                config.BIRD_Y = 0.0
                config.bird_velocity = 0.0
                config.invulnerable = False
                config.speed_multiplier = 1.0
                # REMOVIDO: Reset de last_pipe_bottom_h
                # REMOVIDO: Reset de last_pipe_was_moving

            # Pula se o jogo está rodando
            if config.game_started and not config.game_over:
                config.bird_velocity = config.JUMP_STRENGTH

        # Tecla R (Restart)
        if key == glfw.KEY_R and config.game_over:
            print("Jogo Reiniciado!")
            # Resetar estado completo do jogo para recomeçar
            config.game_over = False
            config.game_started = False # Volta para a tela inicial
            config.lives = config.INITIAL_LIVES
            config.score = 0
            config.pipes.clear()
            config.powerups.clear()
            config.BIRD_Y = 0.0
            config.bird_velocity = 0.0
            config.invulnerable = False
            config.speed_multiplier = 1.0
            config.last_pipe_time = 0 # Reseta timer de spawn
            # REMOVIDO: Reset de last_pipe_bottom_h
            # REMOVIDO: Reset de last_pipe_was_moving