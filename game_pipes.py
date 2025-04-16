# game_pipes.py
from OpenGL.GL import *
import config
import random
import time
# Importar PowerUp para que o random.choice funcione corretamente com a classe
from powerup import PowerUp

def draw_pipes():
    """Desenha os canos na tela (ainda com cores sólidas)."""
    for pipe in config.pipes:
        # Cor verde para os canos
        glColor3f(0.0, 0.6, 0.0) # Um verde um pouco mais escuro

        # Cano Superior
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], 1.0) # Top-Left
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, 1.0) # Top-Right
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['top_height']) # Bottom-Right
        glVertex2f(pipe['x'], pipe['top_height']) # Bottom-Left
        glEnd()

        # Cano Inferior
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], pipe['bottom_height']) # Top-Left
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, pipe['bottom_height']) # Top-Right
        glVertex2f(pipe['x'] + config.PIPE_WIDTH, -1.0) # Bottom-Right (-0.9 é o chão, -1.0 é a base)
        glVertex2f(pipe['x'], -1.0) # Bottom-Left
        glEnd()

def update_pipes(delta_time):
    """Atualiza a posição dos canos, gera novos canos e power-ups, e remove os que saíram da tela."""

    # Move todos os canos existentes para a esquerda
    for pipe in config.pipes:
        pipe['x'] -= config.PIPE_SPEED * config.speed_multiplier * delta_time

    # Remove canos que saíram completamente da tela pela esquerda
    # A condição verifica se a borda direita do cano (pipe['x'] + PIPE_WIDTH) passou da borda esquerda (-1.0)
    config.pipes[:] = [pipe for pipe in config.pipes if pipe['x'] + config.PIPE_WIDTH > -1.0]

    # Gera novos canos e potencialmente power-ups em intervalos regulares
    current_time = time.time()
    # Verifica se o tempo desde o último cano é maior que o intervalo ajustado pela velocidade
    if (config.game_started and not config.game_over and
            current_time - config.last_pipe_time > config.PIPE_SPAWN_INTERVAL / config.speed_multiplier):

        # Calcula a altura da abertura do cano aleatoriamente
        # Define limites para a altura do cano inferior, garantindo espaço para o GAP
        min_bottom_height = -1.0 + 0.2 # Pelo menos 0.2 acima da base da tela
        max_bottom_height = 1.0 - 0.2 - config.PIPE_GAP # Pelo menos 0.2 abaixo do topo e espaço para o gap
        bottom_pipe_h = random.uniform(min_bottom_height, max_bottom_height)
        top_pipe_h = bottom_pipe_h + config.PIPE_GAP # Calcula a altura do cano superior

        # Adiciona o novo par de canos à lista
        new_pipe = {
            'x': 1.0 + config.PIPE_WIDTH, # Começa ligeiramente fora da tela direita
            'top_height': top_pipe_h,
            'bottom_height': bottom_pipe_h,
            'scored': False # Flag para controlar pontuação
        }
        config.pipes.append(new_pipe)

        # Chance de gerar um power-up junto com o cano
        if random.random() < 0.25: # 25% de chance de gerar um power-up
            powerup_type = random.choice(config.POWERUP_TYPES) # Escolhe um tipo aleatório ('life' ou 'speed')
            # Gera o power-up no meio da abertura do cano
            powerup_y = (bottom_pipe_h + top_pipe_h) / 2.0
            # Posição X inicial ligeiramente à frente do cano
            powerup_x = new_pipe['x'] + config.PIPE_WIDTH / 2.0
            config.powerups.append(PowerUp(powerup_x, powerup_y, powerup_type))
            print(f"Gerado PowerUp: {powerup_type} em ({powerup_x:.2f}, {powerup_y:.2f})") # Debug

        config.last_pipe_time = current_time # Atualiza o tempo do último cano gerado


    # Atualiza a posição X dos power-ups (eles se movem junto com os canos)
    for powerup in config.powerups:
        powerup.x -= config.PIPE_SPEED * config.speed_multiplier * delta_time

    # Remove power-ups que foram coletados ou saíram da tela pela esquerda
    # CORREÇÃO APLICADA AQUI: Usar p.collision_size em vez de p.size
    config.powerups[:] = [p for p in config.powerups if not (p.x + p.collision_size < -1.0 or p.collected)]

    # --- Lógica de Pontuação ---
    # Incrementa a pontuação quando o pássaro passa por um cano
    for pipe in config.pipes:
         # Verifica se o pássaro passou da borda direita do cano e ainda não pontuou por este cano
         pipe_right_edge = pipe['x'] + config.PIPE_WIDTH
         if not pipe.get('scored', False) and config.BIRD_X > pipe_right_edge:
              config.score += 1
              pipe['scored'] = True # Marca que pontuou por este cano
              print(f"Pontuação: {config.score}") # Debug