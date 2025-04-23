# input.py
import glfw
import time
import config
import random
import pause # Importa o módulo pause

def key_callback(window, key, scancode, action, mods):
    """Processa eventos de teclado."""
    if action == glfw.PRESS:
        # Tecla ESC (Pause/Unpause)
        if key == glfw.KEY_ESCAPE:
            if config.game_started and not config.game_over:
                if not config.game_paused: # Pausando o jogo
                    config.game_paused = True
                    config.pause_start_time = time.time() # Registra tempo REAL da pausa
                    print("Jogo pausado!")
                else: # Despausando o jogo
                    config.game_paused = False
                    pause_duration = time.time() - config.pause_start_time
                    config.total_pause_duration += pause_duration # Acumula duração da pausa

                    # --- Ajusta tempos de FIM dos efeitos ---
                    # Adiciona a duração da pausa aos tempos finais futuros
                    if config.invulnerable_time > config.pause_start_time: # Ajusta apenas se o fim era no futuro
                        config.invulnerable_time += pause_duration
                    if config.heavy_jump_end_time > config.pause_start_time:
                        config.heavy_jump_end_time += pause_duration
                    if config.shrink_end_time > config.pause_start_time:
                        config.shrink_end_time += pause_duration
                    # --- Fim Ajuste Tempos Fim ---

                    # Ajusta o tempo do ÚLTIMO spawn de cano e nuvem
                    # para que o PRÓXIMO spawn ocorra no intervalo correto após despausar
                    config.last_pipe_time += pause_duration
                    config.last_cloud_spawn_time += pause_duration

                    # Atualiza o tempo do último frame das animações para evitar saltos
                    config.last_frame_time += pause_duration
                    for powerup in config.powerups:
                         powerup.last_frame_time += pause_duration
                    for cloud in config.clouds:
                         cloud.last_frame_time += pause_duration


                    print(f"Jogo continuado! (Pausado por {pause_duration:.1f}s)")


        # Tecla ESPAÇO
        if key == glfw.KEY_SPACE:
            if config.game_paused:
                return # Ignora se pausado

            if not config.game_started:
                print("Jogo Iniciado!")
                config.game_started = True
                # Inicializa tempos baseados no tempo de jogo (que será 0 no início)
                current_game_time = pause.get_game_time() # = 0.0
                config.last_pipe_time = current_game_time
                config.last_cloud_spawn_time = current_game_time # Reseta timer spawn nuvem
                config.next_cloud_spawn_interval = random.uniform(config.CLOUD_SPAWN_INTERVAL_MIN, config.CLOUD_SPAWN_INTERVAL_MAX)
                config.last_frame_time = time.time() # Usa tempo real para animação inicial

                # Resetar estado completo
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
                config.game_paused = False # Garante que não começa pausado
                config.pause_start_time = 0.0
                config.total_pause_duration = 0.0 # Reseta tempo total pausado

            if config.game_started and not config.game_over:
                current_jump_strength = config.JUMP_STRENGTH
                if config.heavy_jump_active:
                    current_jump_strength *= config.HEAVYJUMP_JUMP_MULTIPLIER
                config.bird_velocity = current_jump_strength

        # Tecla R (Restart)
        if key == glfw.KEY_R and config.game_over:
            print("Jogo Reiniciado!")
            # Resetar estado completo
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