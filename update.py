# update.py
import config
import time
from game_pipes import update_pipes # Para atualizar canos e powerups
from collisions import check_collision # Para verificar colisões

def update(delta_time):
    """Atualiza o estado do jogo a cada frame."""

    # --- Atualização da Animação do Pássaro (Sempre que houver textura) ---
    # Fazemos isso mesmo se o jogo não começou ou acabou, para o pássaro 'respirar'
    current_time_anim = time.time()
    if config.bird_texture_id and config.bird_frames_uv: # Verifica se a textura e os frames existem
        if current_time_anim - config.last_frame_time > config.BIRD_ANIMATION_SPEED:
            config.bird_current_frame = (config.bird_current_frame + 1) % len(config.bird_frames_uv)
            config.last_frame_time = current_time_anim

    # Só atualiza a lógica do jogo se ele estiver rodando
    if not config.game_started or config.game_over:
        return # Sai da função se o jogo não está ativo

    # --- Lógica de Física do Pássaro ---
    config.bird_velocity += config.GRAVITY * delta_time # Aplica gravidade
    config.BIRD_Y += config.bird_velocity * delta_time # Atualiza posição Y

    # --- Atualização dos Canos e Power-ups ---
    # A função update_pipes agora também é responsável por mover os powerups
    # e verificar se novos canos/powerups devem ser gerados.
    update_pipes(delta_time)

    # --- Verificação de Colisões ---
    # Verifica colisão com chão, teto, canos e power-ups
    check_collision()

    # --- Gerenciamento de Estados (Invulnerabilidade, Speed Boost) ---
    current_time_state = time.time() # Reobtém o tempo atual
    if config.invulnerable and current_time_state > config.invulnerable_time:
        config.invulnerable = False
        # Se o speed boost estava ativo (identificado pelo multiplicador), reseta-o
        if config.speed_multiplier > 1.0:
            config.speed_multiplier = 1.0
            print("Speed boost acabou.") # Debug