# update.py
import config
import time
from game_pipes import update_pipes # Atualiza canos (posição, geração, remoção) e powerups (posição, remoção)
from collisions import check_collision # Verifica colisões

def update(delta_time):
    """Atualiza o estado completo do jogo a cada frame."""

    # --- Atualização da Animação do Pássaro ---
    # Anima mesmo se o jogo não começou/terminou
    current_time_anim = time.time()
    if config.bird_texture_id and config.bird_frames_uv: # Só anima se houver frames
        if current_time_anim - config.last_frame_time > config.BIRD_ANIMATION_SPEED:
            # Avança o frame, fazendo loop
            config.bird_current_frame = (config.bird_current_frame + 1) % len(config.bird_frames_uv)
            config.last_frame_time = current_time_anim

    # --- Lógica Principal do Jogo (Só executa se o jogo estiver rodando) ---
    if not config.game_started or config.game_over:
        return # Pausa a física, geração de canos, colisões etc.

    # --- Física do Pássaro ---
    config.bird_velocity += config.GRAVITY * delta_time # Aplica gravidade
    config.BIRD_Y += config.bird_velocity * delta_time # Atualiza posição Y

    # --- Atualização dos Canos e Power-ups ---
    # update_pipes move canos H/V, gera novos, move powerups H, remove powerups coletados/fora da tela
    update_pipes(delta_time)

    # --- Verificação de Colisões ---
    # check_collision verifica pássaro vs (chão, teto, canos, powerups)
    # e chama handle_collision ou aplica efeitos de powerup
    check_collision() # Importante chamar DEPOIS de atualizar posições

    # --- Gerenciamento de Estados Pós-Colisão/Powerup ---
    current_time_state = time.time()
    # Verifica se o tempo de invulnerabilidade/boost acabou
    if config.invulnerable and current_time_state > config.invulnerable_time:
        config.invulnerable = False
        # Se o speed boost estava ativo (identificado pelo multiplicador), reseta-o também
        if config.speed_multiplier > 1.0:
            config.speed_multiplier = 1.0
            print("Speed boost acabou.") # Debug
        else:
            print("Invulnerabilidade acabou.") # Debug (se não era speed boost)

    # Poderia adicionar lógica de aumento de dificuldade com o tempo/score aqui
    # Ex: aumentar PIPE_SPEED ou diminuir PIPE_SPAWN_INTERVAL gradualmente