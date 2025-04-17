# collisions.py
import config
import time
from powerup import PowerUp # Para type hinting / isinstance se necessário

def handle_collision():
    """Chamado quando uma colisão fatal (chão, teto, cano) ocorre e o jogador não está invulnerável."""
    # Não faz nada se já estiver game over (evita múltiplas chamadas por frame)
    if config.game_over:
        return

    print("Colisão fatal detectada!")
    config.lives -= 1
    print(f"Vidas restantes: {config.lives}")

    if config.lives <= 0:
        config.game_over = True
        config.bird_velocity = 0 # Para o pássaro ao morrer
        print("Game Over!")
    else:
        # Perdeu uma vida, mas o jogo continua: Reset e invulnerabilidade
        config.BIRD_Y = 0.0 # Reposiciona no centro vertical
        config.bird_velocity = 0.0 # Para a velocidade
        config.invulnerable = True
        # Duração da invulnerabilidade normal (sem power-up)
        invulnerability_duration = 2.0
        config.invulnerable_time = time.time() + invulnerability_duration
        print(f"Perdeu uma vida! Invulnerável por {invulnerability_duration}s.")


def check_collision():
    """Verifica todas as possíveis colisões do pássaro."""
    # Não verifica colisões se o jogo ainda não começou ou já acabou
    if not config.game_started or config.game_over:
        return

    # Calcula bordas de colisão do pássaro (baseado no raio)
    bird_bottom_edge = config.BIRD_Y - config.BIRD_COLLISION_RADIUS
    bird_top_edge = config.BIRD_Y + config.BIRD_COLLISION_RADIUS
    bird_left_edge = config.BIRD_X - config.BIRD_COLLISION_RADIUS
    bird_right_edge = config.BIRD_X + config.BIRD_COLLISION_RADIUS

    # 1. Colisão com Chão e Teto
    # Chão (topo do chão está em -0.9)
    if bird_bottom_edge <= -0.9:
        # print("Colisão com o chão.") # Debug frequente
        if not config.invulnerable:
            handle_collision()
        # Impede de cair mais, mesmo invulnerável (salvo se já for game over)
        if not config.game_over:
            config.BIRD_Y = -0.9 + config.BIRD_COLLISION_RADIUS
            config.bird_velocity = 0 # Para evitar "quicar"
        return # Colisão fatal ou ajuste de posição, não checa mais nada

    # Teto (topo da tela visível é 1.0)
    if bird_top_edge >= 1.0:
        # print("Colisão com o teto.") # Debug frequente
        if not config.invulnerable:
            handle_collision()
        # Impede de subir mais, mesmo invulnerável (salvo se já for game over)
        if not config.game_over:
            config.BIRD_Y = 1.0 - config.BIRD_COLLISION_RADIUS
            config.bird_velocity = max(0, config.bird_velocity) # Evita velocidade negativa prendendo no teto
        return # Colisão fatal ou ajuste de posição

    # 2. Colisão com Power-ups (Verifica ANTES dos canos)
    # Itera sobre cópia para poder modificar a lista original (marcar como coletado)
    for powerup in config.powerups:
        if not powerup.collected:
            # Colisão Círculo-Círculo
            dist_sq = (config.BIRD_X - powerup.x)**2 + (config.BIRD_Y - powerup.y)**2
            radii_sum_sq = (config.BIRD_COLLISION_RADIUS + powerup.collision_size)**2

            if dist_sq < radii_sum_sq:
                print(f"Coletou power-up: {powerup.type}")
                powerup.collected = True # Marca para remoção em update_pipes

                # Aplica efeito
                if powerup.type == 'life':
                    config.lives = min(config.lives + 1, config.INITIAL_LIVES * 2) # Limita vidas
                    print(f"Ganhou vida! Vidas: {config.lives}")
                elif powerup.type == 'speed':
                    config.speed_multiplier = 2.0 # Dobra velocidade do jogo
                    # Speed boost também concede invulnerabilidade
                    config.invulnerable = True
                    boost_duration = 5.0
                    # Se já estava invulnerável, estende pelo tempo do boost
                    config.invulnerable_time = max(config.invulnerable_time, time.time() + boost_duration)
                    print(f"Speed Boost ativado por {boost_duration}s!")

                # A remoção efetiva da lista `config.powerups` acontece em `update_pipes`
                # break # Geralmente só coleta um por frame, mas permite múltiplos se sobrepostos


    # 3. Colisão com Canos
    # Pula a verificação de canos se estiver invulnerável
    if config.invulnerable:
        return

    for pipe in config.pipes:
        pipe_left_edge = pipe['x']
        pipe_right_edge = pipe['x'] + config.PIPE_WIDTH

        # --- Verificação de Colisão AABB (Axis-Aligned Bounding Box) Simplificada ---
        # (Mais simples que círculo vs retângulo, bom o suficiente aqui)

        # 1. Verifica sobreposição Horizontal
        horizontal_overlap = bird_right_edge > pipe_left_edge and bird_left_edge < pipe_right_edge

        if horizontal_overlap:
            # 2. Verifica se colidiu VERTICALMENTE com um dos canos (fora da abertura)
            hit_bottom_pipe = bird_bottom_edge < pipe['bottom_height']
            hit_top_pipe = bird_top_edge > pipe['top_height']

            if hit_bottom_pipe or hit_top_pipe:
                # print("Colisão com cano!") # Debug frequente
                handle_collision()
                return # Para a verificação, só pode colidir com um obstáculo fatal por frame