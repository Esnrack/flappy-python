# pause.py
import config
import time

def get_game_time():
    """Retorna o tempo de jogo 'real', descontando o tempo pausado."""
    # Se o jogo não começou, o tempo de jogo é 0
    if not config.game_started:
        return 0.0

    # Pega o tempo atual do sistema
    current_real_time = time.time()

    # Se o jogo está pausado, o tempo de jogo é o momento em que foi pausado,
    # menos o tempo total que já esteve pausado *antes* desta pausa atual.
    if config.game_paused:
        # Tempo de jogo congelado no momento da pausa
        # pause_start_time já inclui o início do tempo real
        # total_pause_duration é o tempo acumulado de pausas anteriores
        # Precisamos subtrair a base do tempo inicial ou algo assim? Não...
        # O tempo de jogo efetivo é o tempo do relógio quando pausou menos as pausas anteriores.
        # Vamos simplificar: retorna o tempo congelado
        return config.pause_start_time - config.total_pause_duration # <<< Tempo congelado
    else:
        # Se não está pausado, é o tempo real atual menos o tempo total acumulado em pausas.
        return current_real_time - config.total_pause_duration