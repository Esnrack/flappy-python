# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRAVITY = -0.9  # Aceleração da gravidade
JUMP_STRENGTH = 0.5 # Força do pulo
PIPE_WIDTH = 0.15  # Largura visual dos canos
PIPE_GAP = 0.4   # Espaço vertical entre os canos
PIPE_SPEED = 0.5 # Velocidade de movimento dos canos
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.7 # Intervalo para gerar novos canos

# --- Configurações para Sprites ---
BIRD_SPRITE_PATH = "sprites/bird_sheet.png"  # Caminho para a sprite sheet do pássaro
BIRD_COLS = 12  # Número de colunas (frames) na sprite sheet do pássaro
BIRD_ROWS = 1  # Número de linhas na sprite sheet do pássaro
BIRD_ANIMATION_SPEED = 0.1  # Segundos por frame da animação do pássaro

POWERUP_SPRITE_PATH = "sprites/powerups.png" # Caminho para a sprite sheet dos power-ups
POWERUP_COLS = 2 # Ex: 2 tipos de powerups (vida, velocidade)
POWERUP_ROWS = 1
POWERUP_TYPES = ['life', 'speed'] # Ordem correspondente aos sprites na sheet (esquerda para direita, cima para baixo)

# Tamanhos para Desenho (visuais) - Ajuste estes!
BIRD_DRAW_WIDTH = 0.12   # Largura do sprite do pássaro na tela
BIRD_DRAW_HEIGHT = 0.12  # Altura - será ajustada pelo aspect ratio do frame em main.py
POWERUP_DRAW_SIZE = 0.08 # Tamanho do sprite do power-up na tela (largura e altura)

# Tamanho para Colisão - Ajuste para corresponder à área de colisão do sprite
BIRD_COLLISION_RADIUS = 0.045 # Raio para detecção de colisão do pássaro
POWERUP_COLLISION_SIZE = 0.04  # Metade do tamanho (raio) para colisão do power-up

# Variáveis Globais de Jogo
bird_velocity = 0.0
game_started = False
game_over = False
lives = INITIAL_LIVES
score = 0
last_pipe_time = 0.0 # Deve ser float
pipes = []
powerups = []
speed_multiplier = 1.0 # Multiplicador de velocidade (para power-up)
invulnerable = False   # Estado de invulnerabilidade
invulnerable_time = 0.0 # Tempo até quando o pássaro está invulnerável

# Posição inicial do pássaro
BIRD_X = -0.5 # Posição X fixa do pássaro
BIRD_Y = 0.0   # Posição Y inicial do pássaro

# Variáveis Globais para Sprites (serão inicializadas em main.py)
bird_texture_id = None
bird_frames_uv = [] # Lista de tuplas (u0, v0, u1, v1) para cada frame
bird_frame_aspect = 1.0 # Aspect ratio do frame do pássaro
bird_current_frame = 0
last_frame_time = 0.0 # Para controlar a velocidade da animação

powerup_texture_id = None
powerup_uvs = {} # Dicionário: {'life': (u0,v0,u1,v1), 'speed': (...)}
powerup_frame_aspect = 1.0

# (Não precisamos mais de BIRD_SIZE, usamos BIRD_COLLISION_RADIUS e BIRD_DRAW_WIDTH/HEIGHT)

high_score = 0  # Variável para armazenar o recorde atual
HIGH_SCORE_FILE = "high_score.txt"  # Nome do arquivo onde o recorde será salvo